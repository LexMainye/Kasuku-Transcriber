# Dockerfile for Kasuku Transcriber
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    libsndfile1-dev \
    build-essential \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config.toml ./.streamlit/config.toml

# Create necessary directories
RUN mkdir -p /root/.cache/huggingface \
    && mkdir -p /root/.cache/tts \
    && mkdir -p .streamlit

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
ENV TRANSFORMERS_CACHE=/root/.cache/huggingface
ENV HF_HOME=/root/.cache/huggingface
ENV COQUI_TTS_CACHE=/root/.cache/tts
ENV TTS_HOME=/root/.cache/tts
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/healthz || exit 1

# Run the application
CMD ["streamlit", "run", "src/app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--browser.gatherUsageStats=false", \
    "--server.fileWatcherType=none", \
    "--server.maxUploadSize=200"]