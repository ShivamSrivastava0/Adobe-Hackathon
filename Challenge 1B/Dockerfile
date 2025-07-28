FROM --platform=linux/amd64 python:3.10-slim

LABEL maintainer="Your Name <you@example.com>" \
      description="Challenge 1B: Persona‑Driven PDF Analyzer (offline, CPU‑only)"

WORKDIR /app

# System deps for PDF parsing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY modules/ modules/
COPY run_1b.py .

# Ensure instant log flushing
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "run_1b.py"]