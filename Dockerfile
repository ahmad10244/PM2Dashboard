# syntax=docker/dockerfile:1
FROM python:3.9-alpine

WORKDIR /app

RUN apk update --no-cache 
RUN apk upgrade
RUN apk add --no-cache gcc musl-dev linux-headers build-base

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["./gunicorn.sh"]