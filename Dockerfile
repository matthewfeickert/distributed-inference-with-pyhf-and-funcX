FROM python:3.8-buster

RUN apt-get update -y && \
    apt-get install -y \
        gcc \
        python3-dev && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*
COPY core-requirements.txt .
RUN python -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
    python -m pip --no-cache-dir install -r core-requirements.txt
