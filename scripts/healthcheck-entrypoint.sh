#!/bin/sh
set -e

echo "Check microservices availability"
python scripts/service_healthcheck.py --service-name "accounts" --ip "${ACCOUNT_SERVICE_HOST}" --port "${ACCOUNT_SERVICE_PORT}"

echo "Running app with uvicorn"
uvicorn app.main:app --host 0.0.0.0 --port 8080

exec "$@"