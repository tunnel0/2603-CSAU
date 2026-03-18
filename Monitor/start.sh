#!/bin/bash

# Start the monitor script in the background
python monitor.py &

# Start the FastAPI application
python -m uvicorn app:app --host 0.0.0.0 --port 8000
