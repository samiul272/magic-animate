FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

RUN  apt-get update && apt-get install -y \
    software-properties-common python3.10 python3-pip

RUN apt-get update && apt-get install --allow-downgrades -y \
    ffmpeg \
    curl \
    gcc \
    git \
    git-lfs\
    wget \
    unzip \
    python-is-python3

RUN git clone https://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@github.com/samiul272/magic-animate.git
RUN ls .
RUN pip install huggingface_hub
RUN cd magic-animate && git lfs clone https://huggingface.co/zcxu-eric/MagicAnimate
RUN cd magic-animate && python download_model.py
RUN cd magic-animate && pip install -r requirements.txt
RUN cd magic-animate && pip install -r vid2densepose/requirements.txt
RUN pip install firebase-admin
