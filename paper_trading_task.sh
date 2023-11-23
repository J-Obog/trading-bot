#!/bin/bash

curl https://pyenv.run | bash
apt-get update
apt-get install -y python3-pip
python3 -m pip install pipenv 
pipenv shell
python3 test.py