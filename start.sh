#!/usr/bin/env bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-10000}"
