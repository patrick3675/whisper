FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git
RUN pip install flask
RUN pip install Werkzeug
RUN pip install numpy
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install tqdm
RUN pip install more-itertools
RUN pip install transformers>=4.19.0
RUN pip install opencv-python-headless
RUN pip install ffmpeg-python
RUN apt install ffmpeg -y
RUN git clone https://github.com/patrick3675/whisper
WORKDIR whisper/
WORKDIR whisper/
RUN wget https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large.pt
RUN pip install SpeechRecognition
EXPOSE 5000
CMD python app.py
