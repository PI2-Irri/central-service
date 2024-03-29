#!/bin/bash

# Exporting all environment variables to use in crontab
env | sed 's/^\(.*\)$/ \1/g' > /root/env

function_postgres_ready() {
python << END
import socket
import time
import os

port = int(os.environ["POSTGRES_PORT"])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('central-db', port))
s.close()
END
}

echo '======= CHECKING FOR UNINSTALLED PKGs AND INSTALLING'
pip freeze || pip install -r requirements.txt

until function_postgres_ready; do
  >&2 echo "======= POSTGRES IS UNAVAILABLE, WAITING"
  sleep 1
done

echo '=========== RUNNING PIP INSTALL ==========='
python manage.py makemigrations

echo '===========  MAKING MIGRATIONS  ==========='
python manage.py migrate

echo '===========    RUNNING CRON     ==========='
cron

echo '===========   RUNNING SERVER    ==========='
python manage.py runserver 0.0.0.0:4001
