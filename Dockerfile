FROM python:3.12.3-alpine

COPY src/create_release_webhook.py /create_release_webhook.py

ENTRYPOINT ["./create_release_webhook.py"]
