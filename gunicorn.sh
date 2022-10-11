#!/bin/sh

# Check postgresql connection
while ! nc -z postgresql $PG_PORT;
do
    echo 'Wainting for postgresql!';
    sleep 1;
done;
echo 'Connected';

flask db upgrade

gunicorn --chdir /app app:app -b 0.0.0.0:8000