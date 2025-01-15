# Frontend build stage
FROM node:18 as frontend-build

WORKDIR /frontend

COPY frontend/package.json ./ 
RUN npm install

COPY frontend/ ./ 
RUN npm run build

FROM nginx:alpine as frontend-server

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-build /frontend/build /usr/share/nginx/html

EXPOSE 80

FROM python:3.10-slim as backend

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ . 

EXPOSE 8001

CMD ["python", "app.py"]
