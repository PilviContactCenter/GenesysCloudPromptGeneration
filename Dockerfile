# Prompt Studio - Docker Container
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies including Azure Speech SDK requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    libasound2 \
    libssl3 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set OpenSSL environment variable for Azure Speech SDK compatibility
ENV SSL_CERT_DIR=/etc/ssl/certs

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create uploads directory with proper permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Expose port
EXPOSE 5001

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "120", "app:app"]