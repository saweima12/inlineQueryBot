#!/bin/bash

export INLINEBOT_CONFIG="./env.py"
pipenv run sanic inlinebot:app -H 0.0.0.0 -p 8001 -d