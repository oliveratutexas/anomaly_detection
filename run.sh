#!/bin/bash

source ./scripts/venv/bin/activate

pip install -r ./scripts/requirements.txt 

python ./src/process_log.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json
