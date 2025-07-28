import os, json, unicodedata, signal, time, re
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar, LAParams

class TimeoutError(Exception):
    pass

class PDFProcessor:
    def _extract_mupdf_lines(self, file_path):
        import fitz
        doc = fitz.open(str(file_path))
        lines = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")['blocks']
            for b in blocks:
                if 'lines' in b:
                    for l in b['lines']:
                        for s in l['spans']:
                            text = s['text'].strip()
                            if not text or len(text) < 3:
                                continue
                            line_obj = {
                                "text": text,
                                "size": round(s['size'], 1),
                                "bold": 'bold' in s['font'].lower(),
                                "font": s['font'],
                                "color": s.get('color', 0),
                                "align": "center" if abs(s['bbox'][0] - s['bbox'][2]) < 10 else "left",
                                "page": page_num+1,
                                "y0": s['bbox'][1]
                            }
                            lines.append(line_obj)
        return lines
    def _detect_language(self, text):
        from langdetect import detect
        try:
            return detect(text)
        except:
            return "unknown"
    def _cluster_headings(self, lines):
        from sklearn.cluster import DBSCAN
        import numpy as np
        if not lines:
            return []
        X = np.array([[l["size"], l["y0"]] for l in lines])
        db = DBSCAN(eps=2, min_samples=1).fit(X)
        for i, l in enumerate(lines):
            l["cluster"] = int(db.labels_[i])
        return lines
    def _ocr_headings(self, file_path):
        # Fallback OCR for image-based PDFs
        try:
            from pdf2image import convert_from_path
            import pytesseract
            from PIL import Image
        except ImportError:
            return []
        headings = []
        pages = convert_from_path(str(file_path), dpi=200)
        for i, img in enumerate(pages):
            text = pytesseract.image_to_string(img, lang='eng')
            for line in text.split('\n'):
                line = line.strip()
                if not line or len(line) < 3:
                    continue
                # Heuristic: OCR headings are short, capitalized, not ending with punctuation
                if len(line.split()) <= 12 and (line.isupper() or line.istitle()) and not line.endswith('.'):
                    headings.append({"level": "H2", "text": line, "page": i+1})
        return headings
    def _is_heading_candidate(self, line, median_size, prev_y0=None):
        text = line["text"]
        # Remove page numbers, footers, headers, repetitive elements, form fields
        if re.match(r'^(page|thank you|thankyou|copyright|all rights reserved|\d+|name|date|signature|address|form|no\.|reg\.|roll|age|relationship|s\.no)$', text.strip(), re.I):
            return False
        # Heuristic: headings are short, not full sentences, not ending with period, not too many words
        if len(text.split()) > 14:
            return False
        if text.endswith('.') or text.endswith(',') or text.endswith(':'):
            return False
        if sum(1 for c in text if c in '.;,!?') > 2:
            return False
        # Exclude lines with lots of numbers (forms)
        if sum(1 for c in text if c.isdigit()) > 6:
            return False
        # Exclude lines that are too short unless very large/bold
        if len(text.split()) < 2 and not (line["size"] > median_size*1.2 or line["bold"]):
            return False
        # Line spacing: headings often have more vertical space above
        spacing_ok = True
        if prev_y0 is not None and abs(line["y0"] - prev_y0) < 20:
            spacing_ok = False
        # Accept if mostly capitalized or bold or centered or spacing is ok
        is_caps = text.isupper() or (text[0].isupper() and sum(1 for c in text if c.isupper()) > len(text) // 2)
        cues = [line["bold"], line["align"]=="center", is_caps, spacing_ok]
        return any(cues) and line["size"] >= median_size
    def __init__(self, src_folder, dst_folder, timeout=60):
        self.src = Path(src_folder)
        self.dst = Path(dst_folder)
        self.timeout = timeout
        signal.signal(signal.SIGALRM, self._on_timeout)

    def _on_timeout(self, *_):
        raise TimeoutError("Exceeded time limit")

    def _clean_text(self, text):
        txt = unicodedata.normalize("NFKC", text).strip()
        return re.sub(r"[\u200b\u200c\u200d\ufeff]+", "", txt)

    def _parse_lines(self, file_path):
        # Use both pdfminer and PyMuPDF for richer features
        import time
        t0 = time.time()
        lines = self._extract_mupdf_lines(file_path)
        # Optionally merge with pdfminer lines for redundancy
        # lines += ... (pdfminer extraction if needed)
        sizes = [l["size"] for l in lines]
        # Cluster headings for grouping
        lines = self._cluster_headings(lines)
        # Language detection for each line
        for l in lines:
            l["lang"] = self._detect_language(l["text"])
        # Adaptive threshold: use median font size for filtering
        median_size = sorted(sizes)[len(sizes)//2] if sizes else 0
        top_sizes = sorted(set(sizes), reverse=True)[:3]
        filtered_lines = []
        prev_y0 = None
        min_size = median_size * 0.9 if median_size else 0
        for l in lines:
            # Pre-filter: only process lines above min_size or with bold/center cues
            if l["size"] >= min_size or l["bold"] or l["align"] == "center":
                if (l["size"] in top_sizes or l["bold"]):
                    if self._is_heading_candidate(l, median_size, prev_y0):
                        filtered_lines.append(l)
            prev_y0 = l["y0"]
        t1 = time.time()
        return sizes, filtered_lines
        t1 = time.time()
        print(f"[PROFILE] Parsed lines in {t1-t0:.2f}s, kept {len(filtered_lines)} heading candidates.")
        return sizes, filtered_lines
    def _determine_thresholds(self, sizes):
        uniq = sorted(set(sizes), reverse=True)
        # Only return top 3 font sizes for H1, H2, H3
        h1 = uniq[0] if len(uniq) > 0 else 0
        h2 = uniq[1] if len(uniq) > 1 else 0
        h3 = uniq[2] if len(uniq) > 2 else 0
        return h1, h2, h3

    def _classify(self, info, thresholds):
        s = info["size"]
        text = info["text"]
        y0 = info["y0"]
        is_caps = text.isupper() or (text[0].isupper() and sum(1 for c in text if c.isupper()) > len(text) // 2)
        is_top = y0 > 700 if y0 else False
        h1, h2, h3 = thresholds
        if s >= h1 and (info["bold"] or info["align"]=="center" or is_caps or is_top):
            return "H1"
        if s >= h2 and (info["bold"] or info["align"]=="center" or is_caps):
            return "H2"
        if s >= h3 and (is_caps or info["bold"]):
            return "H3"
        return None

    def _clean_outline(self, raw):
        # Merge consecutive heading lines with same style, page, and level
        merged = []
        # Sort by page, then descending y0 (top-to-bottom)
        raw_sorted = sorted(raw, key=lambda x: (x["page"], -x["y0"]))
        prev = None
        for item in raw_sorted:
            t = item["text"]
            if len(t) < 3 or t.lower() in ("contents", "table of contents"): continue
            if prev and (
                item["page"] == prev["page"] and
                item["level"] == prev["level"] and
                abs(item["size"] - prev["size"]) < 0.5 and
                item["bold"] == prev["bold"] and
                item["align"] == prev["align"] and
                abs(item["y0"] - prev["y0"]) < 100
            ):
                # Merge text in top-to-bottom order
                prev["text"] = prev["text"] + " " + t
            else:
                if prev:
                    merged.append({"level": prev["level"], "text": prev["text"], "page": prev["page"]})
                prev = item.copy()
        if prev:
            merged.append({"level": prev["level"], "text": prev["text"], "page": prev["page"]})
        return merged

    def extract_outline(self, file_path):
        sizes, lines = self._parse_lines(file_path)
        h1, h2, h3 = self._determine_thresholds(sizes)
        raw = []
        for ln in lines:
            lvl = self._classify(ln, (h1, h2, h3))
            if lvl:
                raw.append({**ln, "level": lvl})
        # Fallback to OCR if no headings detected
        if not raw:
            print("[INFO] No headings detected via text extraction, running OCR fallback...")
            raw = self._ocr_headings(file_path)
        return self._clean_outline(raw)

    def extract_title(self, file_path):
        _, lines = self._parse_lines(file_path)
        if not lines: 
            return file_path.name
        line = max(lines, key=lambda l:(l["size"], -l["page"]))
        return line["text"] if len(line["text"])>=5 else file_path.name

    def process(self):
        self.dst.mkdir(exist_ok=True)
        for pdf in self.src.glob("*.pdf"):
            try:
                signal.alarm(self.timeout)
                start = time.time()
                outline = self.extract_outline(pdf)
                title   = self.extract_title(pdf)
                data = {"title": title, "outline": outline}
                out_fp = self.dst / (pdf.stem + ".json")
                with open(out_fp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                # Only print summary per file, not per line
                print(f"✔ {pdf.name} → {out_fp} ({time.time()-start:.2f}s)")
                signal.alarm(0)
            except TimeoutError:
                print(f"⌛ Skipped {pdf.name} (timeout)")
            except Exception as err:
                print(f"✖ {pdf.name}: {err}")

if __name__ == "__main__":
    PDFProcessor("/app/input", "/app/output", timeout=60).process()
