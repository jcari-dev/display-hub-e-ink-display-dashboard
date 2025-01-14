FROM python:3.10-slim as backend

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential python3-dev libffi-dev libssl-dev \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python", "app.py"]
