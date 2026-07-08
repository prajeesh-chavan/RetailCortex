FROM python:3.10-slim

RUN apt-get update && apt-get install -y openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY dbt_retail/ dbt_retail/
COPY config/ config/
COPY run_pipeline.py .

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "run_pipeline.py"]
