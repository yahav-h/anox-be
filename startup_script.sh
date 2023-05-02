#!/usr/bin/env bash
source ./venv/bin/activate
./venv/bin/python3 -m pip install requirements.txt
flask run --port 5000