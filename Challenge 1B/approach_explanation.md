# Approach Explanation

## Methodology
This solution is designed to generalize across diverse document types, personas, and tasks. The system processes each collection independently, extracting and ranking sections most relevant to the persona’s job-to-be-done.

### 1. PDF Section Extraction
We use `pdfminer.six` to parse each PDF and extract text lines, identifying headings and sections based on font size, boldness, and alignment. This heuristic approach works across various document layouts, ensuring that major sections (H1, H2, H3) are captured.

### 2. Semantic Ranking
Extracted sections are ranked for relevance using TF-IDF vectorization and cosine similarity. The persona and job description are combined into a query, and each section’s title is scored for semantic similarity to this query. This ensures that the most relevant sections for the persona’s task are prioritized.

### 3. Multi-Collection Processing
The system iterates over all collections in the input directory, processing each according to its configuration. Output is generated in a standardized JSON format, including metadata, ranked sections, and subsection analysis.

### 4. Constraints Handling
- **CPU-only**: All processing is done offline, with no internet access or GPU requirements.
- **Model Size**: Only lightweight models (TF-IDF, no deep learning) are used, keeping dependencies small.
- **Speed**: Efficient parsing and ranking ensure processing time is well within the 60-second limit for typical collections.

### 5. Output Structure
The output JSON includes:
- Metadata (documents, persona, job, timestamp)
- Extracted sections (document, page, title, rank)
- Subsection analysis (document, refined text, page)

## Generalization
The approach is robust to different domains and personas, as it relies on semantic similarity and flexible section extraction. It can handle research papers, guides, reports, and more, adapting to the user’s needs.

## Limitations & Future Work
- Section extraction may miss complex layouts or non-standard headings.
- Subsection analysis is currently based on section titles; future versions could extract finer-grained content.
- More advanced ranking (e.g., transformer models) could be added if resource constraints allow.

---
This methodology ensures relevance, speed, and generalizability for persona-driven document intelligence.
