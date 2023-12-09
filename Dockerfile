FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

RUN  apt-get update && apt-get install -y \
    software-properties-common python3.10 python3-pip

RUN apt-get update && apt-get install --allow-downgrades -y \
    ffmpeg \
    curl \
    gcc \
    git \
    wget \
    unzip \
    python-is-python3

RUN pip install -r requirements.txt