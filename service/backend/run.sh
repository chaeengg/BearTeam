#!/bin/bash

# Exposure
uvicorn  --app-dir exposure --reload --host 0.0.0.0 --port 8000 main:app&

# Camera
uvicorn --app-dir camera --reload --host 0.0.0.0 --port 8001 main:app&

# Model
uvicorn  --app-dir model --reload --host 0.0.0.0 --port 8002 main:app&