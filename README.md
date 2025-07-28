# 🚀 Adobe India Hackathon 2025 — Challenge 1A & 1B Solution Overview

## 🏆 Executive Summary

This repository contains our complete solutions for both Challenge 1A ("Understand Your Document") and Challenge 1B ("Persona-Driven Document Intelligence") of the Adobe India Hackathon 2025. Our goal: to build robust, scalable, and lightning-fast systems that extract meaningful structure and insights from any PDF collection, powering smarter document experiences for real-world users.

---

## 💡 Problem Statements

### Challenge 1A: Outline Extraction
Extract the title and hierarchical headings (H1, H2, H3) from any PDF, outputting a strict JSON schema. PDFs are diverse—varying in layout, language, and format—making accurate, generalizable extraction a major challenge.

### Challenge 1B: Persona-Driven Intelligence
Given a collection of PDFs, a persona, and a job-to-be-done, automatically identify and rank the most relevant sections and subsections for that persona’s needs. This requires deep semantic understanding, cross-document analysis, and adaptability to any domain or user profile.

---

## ⚡ Problems We Faced

- **Messy, Complex PDFs:** Many documents had inconsistent formatting, scanned images, forms, or poster-like layouts. Standard font-size heuristics failed on these.
- **Multilingual Content:** PDFs included non-English text (Hindi, Japanese, etc.), requiring Unicode normalization and language-aware logic.
- **Performance Constraints:** Processing had to be completed in under 10 seconds (Challenge 1A) and 60 seconds (Challenge 1B) for large document sets, with strict memory and CPU limits.
- **No Internet Access:** All models and libraries had to run fully offline in Docker containers.
- **Semantic Relevance:** For Challenge 1B, ranking sections by persona/job relevance required advanced NLP and contextual analysis.

---

## 🛠️ Our Approach

### Challenge 1A
- **Hybrid Extraction:** Combined pdfminer.six and PyMuPDF for rich font/style/position metadata.
- **Multi-Cue Heading Detection:** Used font size, boldness, alignment, capitalization, line spacing, and clustering to robustly identify headings.
- **Adaptive Logic:** Dynamically tuned thresholds per document, with fallback to OCR (pytesseract) for scanned/image-based PDFs.
- **Multilingual Support:** Integrated langdetect and Unicode normalization.
- **Lightning Speed:** Optimized all code for single-pass, in-memory processing; disabled debug logs for production runs.

### Challenge 1B — Technologies & Features
- **PDF Parsing:** Used `pdfminer.six` and `pdfplumber` for robust, layout-aware text extraction from diverse PDFs.
- **Persona & Task Mapping:** Input JSONs define persona roles and concrete job-to-be-done, driving relevance scoring.
- **Multilingual Support:** Unicode normalization and language-agnostic TF-IDF ranking ensure extraction works for any language (Hindi, Japanese, etc.).
- **Section & Subsection Extraction:** Custom logic identifies section boundaries and granular subsections, even in noisy documents.
- **Semantic Ranking:** Used `scikit-learn`’s TF-IDF vectorizer and cosine similarity to rank sections by relevance to persona/task.
- **Batch & Multi-Collection Processing:** Automatically processes multiple document collections in parallel, scaling to any domain.
- **Strict Output Schema:** Outputs fully compliant JSON with metadata, ranked sections, and refined subsection analysis.
- **Resource Constraints:** Runs fully offline, on CPU only, with model size <1GB and <60s processing time for 3–5 docs.
- **Dockerized Pipeline:** All dependencies and code run in a reproducible Docker container for easy deployment and judging.

---

## 🎯 Why Our Solution Stands Out

- **Generalization:** Works on any PDF, any language, any domain—no hardcoded logic.
- **Accuracy:** Advanced ML and heuristics deliver high heading/section detection precision and recall.
- **Speed:** Meets all hackathon time and resource constraints.
- **Engineering Excellence:** Modular, Dockerized, and ready for real-world deployment.

---

## 👥 Team Members

- Shivam Srivastava — Team Leader (shivamsrivastava5095@gmail.com)
- Aditya Kumar Singh (aditya45245@gmail.com)
- Ankur Kumar (ak7372840611@gmail.com)

---

## 📂 Folder Structure

/
├── Challenge_1A/
│   ├── Dockerfile
│   ├── process_pdfs.py
│   └── ...
├── Challenge_1B/
│   ├── Dockerfile
│   ├── run_1b.py
│   ├── modules/
│   │   ├── pdf_utils.py
│   │   └── semantic_ranker.py
│   ├── requirements.txt
│   ├── approach_explanation.md
│   ├── Collection_1/
│   │   ├── PDFs/
│   │   ├── challenge1b_input.json
│   │   └── challenge1b_output.json
│   ├── Collection_2/
│   │   ├── PDFs/
│   │   ├── challenge1b_input.json
│   │   └── challenge1b_output.json
│   ├── Collection_3/
│   │   ├── PDFs/
│   │   ├── challenge1b_input.json
│   │   └── challenge1b_output.json
│   └── output/
└── README.md  # (this file)


---

## 🐳 Docker Usage

**Build the Docker image:**
```sh
docker build -t challenge1b .

Run the Docker container:

docker run --rm -v "${PWD}:/app/input" -v "${PWD}/output:/app/output" challenge1b

🧪 How to Test
1. Place your PDFs in each collection’s PDFs folder, matching the filenames in challenge1b_input.json.
2. Activate your Python environment and install requirements:
pip install -r requirements.txt
3. Run the analysis:
python run_1b.py
4. Or use Docker as shown above.
Check the output JSONs in the output folder or in each collection folder.

We built these solutions to tackle the hardest document intelligence problems—so Adobe and the judges can trust our systems to deliver perfect results, every time, for any user and any document.
