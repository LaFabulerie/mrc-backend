#!/bin/bash

python /app/manage.py migrate

python /app/manage.py import

python /app/manage.py collectstatic --noinput

gunicorn mrc.wsgi:application -b 0.0.0.0:8000 -w 2 &


# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $
