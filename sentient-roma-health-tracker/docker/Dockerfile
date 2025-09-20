FROM python:3.11-slim

WORKDIR /app

# Install system dependencies & CA certs for pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Configurable pip settings
ARG PIP_INDEX_URL=https://pypi.org/simple
ARG PIP_TIMEOUT=180
ENV PIP_DEFAULT_TIMEOUT=${PIP_TIMEOUT}

COPY requirements.txt .

# Install Python dependencies with retries
RUN pip install --no-cache-dir --retries 10 --index-url ${PIP_INDEX_URL} -r requirements.txt

COPY . .

ENV HOST=0.0.0.0 PORT=8000
EXPOSE 8000

CMD ["uvicorn", "sentient_roma_api:app", "--host", "0.0.0.0", "--port", "8000"]

