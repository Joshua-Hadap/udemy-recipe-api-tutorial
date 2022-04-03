FROM python:3.10.4-alpine3.15
MAINTAINER Joshua Hadap

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN adduser -D user
USER user