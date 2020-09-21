FROM python:3.7.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY setup.py /
RUN python /setup.py install

COPY . /
WORKDIR /





