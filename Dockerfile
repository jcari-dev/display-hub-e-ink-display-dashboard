FROM node:18 as frontend-build

WORKDIR /frontend

COPY frontend/package.json ./ 
RUN npm install

COPY frontend/src/ ./  # Make sure to copy the src directory as well
RUN npm run build  # This should generate the build files


FROM nginx:alpine as frontend-server

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-build /frontend/dist /usr/share/nginx/html  # Assuming 'dist' is the output directory

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
