FROM python:3.7.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MECAB_PATH "/usr/local/lib/libmecab.so"
ENV MECAB_CHARSET "euc-jp"

RUN apt-get update && apt-get install --reinstall -y apt-utils build-essential dialog netcat gcc wget
RUN pip install -U pip setuptools wheel cymem numpy Cython
RUN pip install sudachipy sudachidict_core mecab-python3 unidic-lite

COPY setup.py /
RUN python /setup.py install

COPY . /
WORKDIR /





