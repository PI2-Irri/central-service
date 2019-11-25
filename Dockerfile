FROM python:3.6

RUN apt-get update && apt-get install -y cron

COPY . /central-service

WORKDIR /central-service

# Setting cron
COPY cronjob /etc/cron.d/cronjob

RUN chmod 0644 /etc/cron.d/cronjob

RUN /usr/bin/crontab /etc/cron.d/cronjob

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt
