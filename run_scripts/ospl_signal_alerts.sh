#!/usr/bin/env bash

# Loading the environment variables
export `cat .env | xargs`
python ospl_signal.py