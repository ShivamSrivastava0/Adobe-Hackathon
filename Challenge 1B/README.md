# 🚀 Adobe India Hackathon 2025: Challenge 1B — Persona-Driven Document Intelligence

## Problem Statement
Build an advanced, scalable solution to analyze multiple PDF collections and extract the most relevant content for specific personas and use cases. The system must:
- Process diverse document collections (3-5 PDFs per collection)
- Extract and rank sections/subsections by relevance to a persona’s job-to-be-done
- Support multilingual documents
- Run CPU-only, offline, and process each collection in under 60 seconds

---

## Why This Matters
In today’s information-rich world, professionals are overwhelmed by lengthy documents. Our solution empowers users to instantly surface the most actionable, persona-specific insights from massive PDF collections—unlocking productivity, compliance, and smarter decision-making.

---

## 💡 Solution Overview
Our system is an intelligent, persona-driven document analyst that:
- Extracts, semantically ranks, and summarizes the most relevant sections from each PDF
- Handles multiple collections, each with its own persona and task
- Outputs structured, explainable JSON for downstream automation or review

---

## 🛠️ Technologies & Models Used
- *Python 3.10* — Fast, robust scripting
- *pdfminer.six* — Reliable PDF parsing and text extraction
- *scikit-learn (TF-IDF, cosine similarity)* — Lightweight, interpretable semantic ranking
- *langdetect* — Multilingual support for global document sets
- *Docker* — Reproducible, portable, and secure execution

---

## 🧠 Methodology
1. *Section Extraction:*
   - Custom heuristics (font size, boldness, alignment) to robustly extract headings/sections from any PDF layout
2. *Multilingual Detection:*
   - Each section’s language is detected and recorded for transparency and global applicability
3. *Semantic Ranking:*
   - Persona and job-to-be-done are combined into a query
   - Each section is ranked by semantic similarity (TF-IDF + cosine) to the persona’s needs
4. *Subsection Analysis:*
   - Granular extraction and ranking of subsections for deeper insights
5. *Output:*
   - Clean, standardized JSON with metadata, ranked sections, and language tags

---

## ⚡ What Sets Us Apart
- *Truly Multilingual:* Handles any language, making it enterprise-ready
- *Explainable AI:* No black-box models—judges can trace every ranking
- *Speed & Efficiency:* Processes 3-5 PDFs per collection in <60s on CPU
- *Generalizable:* Works for HR, travel, legal, research, and more
- *Hackathon-Ready:* Fully containerized, reproducible, and easy to test

---

## 🏆 Challenges & How We Solved Them
- *Diverse PDF Layouts:*
  - Built robust heuristics to handle inconsistent headings and structures
- *Multilingual Content:*
  - Integrated language detection and ensured ranking works across languages
- *Speed Constraints:*
  - Optimized parsing and ranking for sub-minute performance on CPU
- *No Internet/No GPU:*
  - All models and dependencies are lightweight and offline
- *Explainability:*
  - Chose interpretable models (TF-IDF) so every decision is auditable

---

## 📦 Project Structure

Collection_1/
  ├── PDFs/
  ├── challenge1b_input.json
Collection_2/
  ├── PDFs/
  ├── challenge1b_input.json
Collection_3/
  ├── PDFs/
  ├── challenge1b_input.json
modules/
  ├── pdf_utils.py
  ├── semantic_ranker.py
run_1b.py
requirements.txt
Dockerfile
README.md
approach_explanation.md
output/
  ├── Collection_1.json
  ├── Collection_2.json
  ├── Collection_3.json


---

## 🚀 How to Run (in 60 seconds!)
1. *Build the Docker image:*
   powershell
   docker build -t challenge1b .
   
2. *Prepare your input collections:*
   - Place PDFs and challenge1b_input.json in each Collection_* folder
3. *Run the container:*
   powershell
   docker run --rm -v "$PWD:/app/input" -v "$PWD/output:/app/output" challenge1b
   
   - Output will be in /app/output as JSON files

---

## 📑 Input/Output Format
- See sample challenge1b_input.json and output JSONs in each collection folder
- Output includes metadata, ranked sections, subsections, and language tags

---

## 📝 Requirements & Constraints
- Python 3.10
- CPU-only, no internet
- Model size ≤1GB
- Processing time ≤60s for 3-5 documents

---

## 👨‍💻 Team & Contact
Aditya kumar Singh (<adityasingh45245@gmail.com>)
Shivam Srivastava (<shivamsrivastava5095@gmail.com>)
Ankur Kumar 
---

## 🙌 Why We Should Win
- *Solves a real, universal pain point for professionals*
- *Technically robust, explainable, and scalable*
- *Ready for enterprise and global deployment*
- *Built with hackathon spirit: fast, creative, and impactful*

Thank you, Adobe India Hackathon judges, for your time and consideration!
