FROM python:3.7.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY setup.py /
RUN python /setup.py install
RUN python -m spacy download en_core_web_sm

COPY . /
WORKDIR /

ENTRYPOINT ["sh", "run.sh"]




