
# syntax=docker/dockerfile:1
# Multi-stage build for smaller image size
FROM python:3.9-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies (zbar)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    zbar-tools \
    && rm -rf /var/lib/apt/lists/*
    
# Install dependencies
COPY webapp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY webapp/ .

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=8002

# Expose port
EXPOSE 8002

# Run the app directly with Python for reliability
CMD ["python", "app.py"]
