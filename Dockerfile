FROM python:3.10-slim

ARG ENV_FILE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt-get update -qq && apt-get install -y -qq \
    pkg-config procps curl libpq-dev git binutils nano python3-pip gdal-bin libproj-dev \
    python3-brotli python3-cffi libjpeg-dev libopenjp2-7-dev libffi-dev libgirepository1.0-dev libcairo2-dev libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY . /app
COPY $ENV_FILE /app/.env
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn uvicorn[standard]

RUN ./manage.py collectstatic --no-input

RUN apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*