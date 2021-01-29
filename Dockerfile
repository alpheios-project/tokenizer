FROM python:3.7.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --reinstall -y build-essential && apt-get install -y apt-utils && apt-get install -y netcat && apt-get install -y gcc
RUN pip install Cython

COPY setup.py /
RUN python /setup.py install

COPY . /
WORKDIR /





