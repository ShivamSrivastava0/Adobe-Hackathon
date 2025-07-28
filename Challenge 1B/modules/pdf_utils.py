# modules/pdf_utils.py

import unicodedata
import re
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar, LAParams

def _clean(s):
    s = unicodedata.normalize("NFKC", s).strip()
    return re.sub(r"[\u200b\ufeff]", "", s)

def extract_outline(pdf_path):
    sizes, lines = [], []
    for page in extract_pages(str(pdf_path), laparams=LAParams()):
        for block in page:
            if isinstance(block, LTTextContainer):
                for line in block:
                    if isinstance(line, LTTextLine):
                        text = _clean(line.get_text())
                        if not text:
                            continue
                        fs = max((c.size for c in line if isinstance(c, LTChar)), default=0)
                        bold = any("bold" in c.fontname.lower() for c in line if isinstance(c, LTChar))
                        align = "center" if abs(line.x1 - line.x0 - 300) < 150 else "left"
                        lines.append({
                            "text": text,
                            "size": fs,
                            "bold": bold,
                            "align": align,
                            "y0": line.y0,
                            "page": page.pageid
                        })
                        sizes.append(fs)
    uniq = sorted(set(sizes), reverse=True)
    h1, h2, h3 = (uniq + [0, 0, 0])[:3]
    raw = []
    for ln in lines:
        lvl = ("H1" if ln["size"] >= h1
               else "H2" if ln["size"] >= h2 and (ln["bold"] or ln["align"]=="center")
               else "H3" if ln["size"] >= h3
               else None)
        if lvl:
            raw.append({
                "document": Path(pdf_path).name,
                "page_number": ln["page"],
                "section_title": ln["text"],
                "size": ln["size"],
                "y0": ln["y0"],
                "level": lvl
            })
    seen, out = set(), []
    for it in sorted(raw, key=lambda x:(x["page_number"], x["y0"])):
        key = (it["document"], it["section_title"], it["page_number"], it["level"])
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "document": it["document"],
            "page_number": it["page_number"],
            "section_title": it["section_title"],
            "level": it["level"]
        })
    return out
