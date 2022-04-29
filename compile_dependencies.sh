#!/bin/bash

base_image="python:3.8-buster"
docker pull "${base_image}"

cat core-requirements.txt jax-requirements.txt > requirements.txt

docker run --rm \
    -v $PWD:/read \
    "${base_image}" /bin/bash -c 'python -m venv venv && \
    . venv/bin/activate && \
    command -v python &&
    python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --upgrade pip-tools && \
    cp /read/requirements.txt . && \
    pip-compile --generate-hashes --output-file requirements.lock requirements.txt && \
    cp requirements.lock /read/'

# Make sure the file is under user control
cp requirements.lock tmp.lock && mv --force tmp.lock requirements.lock
