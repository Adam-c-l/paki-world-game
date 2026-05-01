FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libgeoip-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with updated versions
RUN pip install --no-cache-dir \
    GeoIP==1.3.2 \
    pyOpenSSL==24.0.0 \
    SQLAlchemy==1.4.52 \
    Twisted==24.3.0 \
    automat==22.10.0 \
    constantly==23.10.4 \
    hyperlink==21.0.0 \
    incremental==22.10.0 \
    zope.interface==6.4

# Copy application code
COPY . .

# Expose lobby and NAT punch ports
EXPOSE 8200 8201

# Make init script executable and run it
RUN chmod +x init_and_run.py

# Use SQLite for simplicity (state persists in Render disk)
CMD ["python", "./init_and_run.py"]
