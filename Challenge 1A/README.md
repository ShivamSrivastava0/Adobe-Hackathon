# Adobe India Hackathon 2025 — Challenge 1A

## 📝 Overview

This repository contains the solution for Challenge 1A of the Adobe India Hackathon 2025.  
The task is to extract structured content from PDF documents — including the title and outline (H1–H3 headings with level, text, and page number) — and output the result in a strict JSON schema format.

The solution is:

- ✅ Fully offline (no internet access required)
- ✅ Fast (≤10s for 50-page PDFs)
- ✅ Dockerized (runs inside a secure container)
- ✅ Supports multilingual PDFs (e.g. Japanese)
- ✅ Conforms to output_schema.json provided by Adobe

---

## 📁 Folder Structure

Challenge_1a/
├── Dockerfile
├── requirements.txt
├── process_pdfs.py
├── input/
│ └── <PDF files to be processed>
├── output/
│ └── <Generated JSONs will appear here>
---

## 🚀 How to Run

### 1. Build the Docker Image

Make sure you are in the Challenge_1a directory.

```bash
docker build -t challenge1a .
### 2. Run the Container

Run the following command from the project root to process PDFs:

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none challenge1a
```

This will process all PDFs in the `input/` folder and write JSONs to `output/`.

---

## 🧠 Heading Detection Logic

The script uses font size analysis to infer heading levels:
- The three most common font sizes are mapped to H1, H2, and H3 (largest = H1).
- Headings are detected by matching text lines with these font sizes.
- The output JSON includes the heading level ("H1", "H2", "H3"), text, and page number.

No hardcoded heading text or file-specific logic is used. The solution works fully offline and supports multilingual PDFs.
