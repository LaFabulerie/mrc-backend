FROM python:3.9-slim-bullseye

ARG STAGE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt-get update -qq && apt-get install -y -qq \
    procps curl libpq-dev git binutils nano python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY . /app
COPY .env.$STAGE /app/.env
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN python manage.py collectstatic --no-input
RUN chmod +x /app/start.sh

RUN apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

CMD ["/app/start.sh"]
