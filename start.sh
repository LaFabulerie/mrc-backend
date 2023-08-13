#!/bin/bash

python /app/manage.py migrate

gunicorn mrc.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 -w 2 &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $