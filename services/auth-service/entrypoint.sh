#!/bin/sh
set -e

# Wait for DB to be ready (simple sleep for now, could be wait-for-it)
sleep 5

# Run migrations
alembic upgrade head

# Start app
uvicorn main:app --host 0.0.0.0 --port 8001
