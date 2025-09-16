# syntax=docker/dockerfile:1
FROM python:3.9-slim

WORKDIR /app

COPY webapp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY webapp/ .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8002

EXPOSE 8002

CMD ["flask", "run", "--host=0.0.0.0", "--port=8002"]
