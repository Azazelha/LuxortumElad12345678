#!/bin/bash
export FLASK_APP=ultra_simple.py
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=8000