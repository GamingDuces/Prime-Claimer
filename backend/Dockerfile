FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget gnupg curl && \
    pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m playwright install --with-deps

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN pip install gunicorn

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:${PORT}", "--workers", "4"]
# This Dockerfile sets up a Python environment with necessary dependencies for a web application.
# It installs system packages, Python dependencies, and sets up the application to run with Gunicorn