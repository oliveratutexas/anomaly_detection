#!/bin/bash


python -m cProfile -s tottime ./src/process_log.py ./log_input/batch_log.json ./log_input/stream_log.json ./log_output/flagged_purchases.json

