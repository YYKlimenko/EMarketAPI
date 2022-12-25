FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LOGIN_DB 'postgres'
ENV PASSWORD_DB 'YuraMarketPassword___1984'
ENV SECRET_KEY  'KYKOYAKO'

WORKDIR /backend
COPY ../requirements.txt /backend/
RUN pip install -r /backend/requirements.txt

COPY .. /backend