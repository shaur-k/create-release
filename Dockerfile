FROM python:3.12.3-alpine

COPY src/create_release_webhook.py /create_release_webhook.py
COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENTRYPOINT ["./create_release_webhook.py"]
