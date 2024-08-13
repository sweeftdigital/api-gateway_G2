FROM python:3.10.12 AS build

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /api-gateway

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/
COPY scripts/ scripts/
COPY tests/ tests/

RUN chmod +x /api-gateway/scripts/healthcheck-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/api-gateway/scripts/healthcheck-entrypoint.sh"]
