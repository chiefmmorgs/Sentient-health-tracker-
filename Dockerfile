FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN test -d external/ROMA || (echo "ROMA submodule missing" && exit 1)

EXPOSE 8000
CMD ["uvicorn", "api.sentient_roma_api:app", "--host", "0.0.0.0", "--port", "8000"]
