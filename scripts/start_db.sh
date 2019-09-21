#!/bin/bash

# Exporting all environment variables to use in crontab
env | sed 's/^\(.*\)$/ \1/g' > /root/env

while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -q -U $POSTGRES_USER; do
  >&2 echo "Postgres is unavailable - sleeping...";
  sleep 5;
done;
>&2 echo "Postgres is up - executing commands...";

postgres
