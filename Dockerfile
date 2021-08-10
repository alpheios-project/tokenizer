FROM python:3.7.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --reinstall -y apt-utils build-essential dialog netcat gcc 
RUN pip install -U pip setuptools wheel cymem numpy Cython
RUN pip install sudachipy sudachidict_core mecab-python3 unidic-lite 

COPY setup.py /
RUN python /setup.py install

COPY . /
WORKDIR /





