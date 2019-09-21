FROM python:3.6

WORKDIR /central-service

COPY . /central-service

RUN pip install --no-cache-dir -r requirements.txt
