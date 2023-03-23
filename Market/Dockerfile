# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR .
ENV DJANGO_SETTINGS_MODULE=hw.settings
ENV PYTHONUNBUFFERED=1

RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrape pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .
