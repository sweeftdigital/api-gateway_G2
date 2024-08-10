FROM python:3.10.12 AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /api-gateway

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000