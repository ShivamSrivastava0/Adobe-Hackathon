FROM python:3.10-slim

# Set working directory
WORKDIR /app 

# Install required system packages for pdfminer
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy main script
COPY process_pdfs.py ./process_pdfs.py

# Run the script on container start
CMD ["python", "process_pdfs.py"]
