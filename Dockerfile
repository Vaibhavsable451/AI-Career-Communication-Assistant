FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Install system dependencies (libgomp1 is required by faiss-cpu on Debian)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for efficient Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY . .

# Zoho Catalyst AppSail default port
EXPOSE 9000

# Start Streamlit listening on the dynamic AppSail port (defaults to 9000)
CMD ["sh", "-c", "streamlit run app.py --server.port=${X_ZOHO_CATALYST_LISTEN_PORT:-9000} --server.address=0.0.0.0 --server.headless=true"]
