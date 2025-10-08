# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY requirements.txt .

# Install only what's absolutely necessary
RUN pip install --user --no-cache-dir \
    streamlit==1.28.0 \
    torch==2.0.1+cpu \
    torchaudio==2.0.2+cpu \
    transformers==4.35.0 \
    librosa==0.10.1 \
    numpy==1.24.3

# Stage 2: Runtime  
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y

COPY --from=builder /root/.local /root/.local
COPY src/ ./src/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/src
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache

# Remove unnecessary files
RUN find /usr/local -name '*.pyc' -delete && \
    find /usr/local -name '__pycache__' -delete

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
