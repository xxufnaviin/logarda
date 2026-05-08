FROM python:3.10

WORKDIR /ingestion

ENV PYTHONPATH=".:./logs:./metrics:$PYTHONPATH" 

COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python"]
