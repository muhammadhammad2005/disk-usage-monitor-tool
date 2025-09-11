FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files (exclude CSV)
COPY main.py mylinux.json ./

# Run script by default
CMD ["python3", "main.py"]
