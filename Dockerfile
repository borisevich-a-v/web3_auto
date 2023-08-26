FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY crypto /app
COPY .env .env

CMD ["python", "main.py"]
