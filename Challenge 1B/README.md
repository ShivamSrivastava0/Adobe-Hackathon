# Challenge 1B: Persona-Driven Document Intelligence

## Overview
This project is an intelligent document analyst that extracts and prioritizes the most relevant sections from collections of PDFs, tailored to a specific persona and their job-to-be-done. It supports multiple collections, each with its own persona, task, and set of documents.

## Features
- Persona-based content analysis
- Importance ranking of extracted sections
- Multi-collection document processing
- Structured JSON output with metadata
- CPU-only, offline execution

## Project Structure
```
Challenge_1b/
├── Collection_1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_2/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection_3/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── modules/
│   ├── pdf_utils.py
│   └── semantic_ranker.py
├── run_1b.py
├── requirements.txt
├── Dockerfile
├── README.md
└── approach_explanation.md
```

## How to Run
1. Build the Docker image:
   ```powershell
   docker build -t challenge1b .
   ```
2. Prepare your input collections in `/Collection_1`, `/Collection_2`, etc.
3. Run the container:
   ```powershell
   docker run --rm -v "$PWD:/app/input" -v "$PWD:/app/output" challenge1b
   ```
   Output will be in `/app/output` as JSON files.

## Input/Output Format
See the sample `challenge1b_input.json` and expected `challenge1b_output.json` in each collection folder.

## Requirements
- Python 3.10
- CPU-only, no internet
- Model size ≤1GB
- Processing time ≤60s for 3-5 documents

## Contact
Maintainer: Your Name <you@example.com>
