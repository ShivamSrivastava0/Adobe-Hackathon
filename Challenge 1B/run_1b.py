# run_1b.py

import os
import warnings
import json
import time
from datetime import datetime
from pathlib import Path
from modules.pdf_utils import extract_outline
from modules.semantic_ranker import rank_sections

INPUT_ROOT = Path(".")  # Use current directory for local runs
OUTPUT_ROOT = Path("output")  # Output will be written to ./output

def load_config(folder):
    fn = folder / "challenge1b_input.json"
    return json.loads(fn.read_text(encoding="utf-8"))

def write_output(folder_name, metadata, sections, subsections):
    out = {
        "metadata": metadata,
        "extracted_sections": [
            {
                "document": s["document"],
                "page_number": s["page_number"],
                "section_title": s["section_title"],
                "importance_rank": s["importance_rank"]
            } for s in sections
        ],
        "subsection_analysis": [
            {
                "document": s["document"],
                "refined_text": s["section_title"],
                "page_number": s["page_number"]
            } for s in sections
        ]
    }
    p = OUTPUT_ROOT / f"{folder_name}.json"
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")

def process_collection(col_dir):
    # Check for valid input file
    input_file = col_dir / "challenge1b_input.json"
    if not input_file.exists():
        print(f"Skipping {col_dir}: No challenge1b_input.json found.")
        return
    try:
        cfg = load_config(col_dir)
    except Exception as e:
        print(f"Skipping {col_dir}: Error loading input JSON - {e}")
        return
    docs = cfg.get("documents", [])
    persona = cfg.get("persona", {}).get("role", "Unknown Persona")
    job = cfg.get("job_to_be_done", {}).get("task", "Unknown Task")
    secs = []
    for d in docs:
        pdf = col_dir / "PDFs" / d["filename"]
        if not pdf.exists():
            print(f"Warning: PDF not found: {pdf}")
            continue
        try:
            secs += extract_outline(pdf)
        except Exception as e:
            print(f"Error extracting from {pdf}: {e}")
    if not secs:
        print(f"No sections extracted for {col_dir.name}. Skipping output.")
        return
    ranked = rank_sections(secs, persona, job)
    metadata = {
        "input_documents": [d["filename"] for d in docs],
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    write_output(col_dir.name, metadata, ranked, ranked)

def main():
    # Suppress PDF parsing warnings for cleaner output
    warnings.filterwarnings("ignore")
    try:
        import logging
        logging.getLogger("pdfminer").setLevel(logging.ERROR)
    except Exception:
        pass
    start = time.time()
    # Process every folder in INPUT_ROOT
    for col in INPUT_ROOT.iterdir():
        if col.is_dir():
            process_collection(col)
    elapsed = time.time() - start
    print(f"Done in {elapsed:.2f}s")

if __name__ == "__main__":
    OUTPUT_ROOT.mkdir(exist_ok=True)
    main()
