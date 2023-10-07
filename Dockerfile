FROM python:3.11-slim-bookworm

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR app

COPY app/ ./
COPY crypto/ ./crypto

CMD ["python", "main.py"]