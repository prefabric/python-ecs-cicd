# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app/ app/

EXPOSE 80
CMD gunicorn -w 4 app:app -b 0.0.0.0:80
