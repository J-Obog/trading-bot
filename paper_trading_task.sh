#!/bin/bash

apt-get update
apt-get install -y python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install pipenv
python3 -m pipenv install
python3 -m pipenv run python3 trade.py
python3 -m pipenv run python3 sync.py