#!/bin/bash
# Start the FastAPI backend server

echo "Starting Bayerische Datenwerke backend API server..."
cd "$(dirname "$0")"
uvicorn main:app --reload --host 0.0.0.0 --port 8000