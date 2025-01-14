# Base image
FROM python:3.10-slim as backend


WORKDIR /app


COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY backend/ .


FROM node:18 as frontend-build

WORKDIR /frontend
COPY frontend/package.json
RUN npm install
COPY frontend/ ./
RUN npm run build


FROM python:3.10-slim
WORKDIR /app


COPY --from=backend /app /app


COPY --from=frontend-build /frontend/build /app/frontend

# Expose port 8000 for the frontend
EXPOSE 8000


CMD ["python", "app.py"]
