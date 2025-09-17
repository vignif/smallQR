# syntax=docker/dockerfile:1
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies (zbar)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    zbar-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY webapp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY webapp/ .

# Environment variables for Flask / Gunicorn
ENV FLASK_ENV=production
ENV PORT=8002
ENV BASE_PATH=/smallqr

# Expose port
EXPOSE 8002

ENV PYTHONUNBUFFERED=1

# Run with Gunicorn (4 workers)
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8002", "--capture-output", "app:app"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8002", "app:app", "--capture-output", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-"]
