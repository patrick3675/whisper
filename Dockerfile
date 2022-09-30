FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/gradient-ai/whisper
RUN pip install flask
RUN pip install Werkzeug
RUN pip install numpy
RUN pip3 install torch torchvision torchaudio
RUN pip install tqdm
RUN pip install more-itertools
RUN pip install transformers>=4.19.0
RUN pip install ffmpeg-python==0.2.0
RUN pip install opencv-python-headless
RUN pip install ffmpeg-python==0.2.0
WORKDIR whisper/
WORKDIR whisper/

EXPOSE 5000
