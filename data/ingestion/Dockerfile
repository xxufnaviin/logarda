FROM python:3.10

WORKDIR /ingestion

ENV PYTHONPATH=".:$PYTHONPATH" 

COPY metrics/metrics_collector.py ./metrics/
COPY logs/logs_collector.py ./logs/
COPY utils/ ./utils/
COPY config/ ./config/

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python"]
