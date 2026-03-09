#!/usr/bin/env bash

source venv/bin/activate
uvicorn VACATIONVAULTNG:app --host 0.0.0.0 --port 8000 --reload
