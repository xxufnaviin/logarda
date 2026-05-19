FROM python:3.10

WORKDIR /ingestion

ENV PYTHONPATH=".:./logs:./metrics:$PYTHONPATH" 

COPY ./data/ingestion/ .
COPY ./utils ./utils
COPY ./config ./config

RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python"]
