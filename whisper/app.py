import io
import json
import argparse
import cv2
import glob
import numpy as np
import os
import sys
from os import listdir
from os.path import isfile, join
from werkzeug.utils import secure_filename
import subprocess
import shutil
from transcribe import cli
import speech_recognition as sr
import torch
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
from PIL import Image
import sys


import argparse
import os
import warnings
from typing import List, Optional, Tuple, Union, TYPE_CHECKING

import numpy as np
import torch
import tqdm

from audio import SAMPLE_RATE, N_FRAMES, HOP_LENGTH, pad_or_trim, log_mel_spectrogram
from decoding import DecodingOptions, DecodingResult
from tokenizer import LANGUAGES, TO_LANGUAGE_CODE, get_tokenizer
from utils import exact_div, format_timestamp, optional_int, optional_float, str2bool, write_txt, write_vtt, write_srt


UPLOAD_FOLDER = 'inputs/audio'
ALLOWED_EXTENSIONS = {'mp3', 'm4a', 'FLAC', 'wav'}
able = ['mp3', 'FLAC', 'wav', 'm4a']

app = Flask(__name__, static_folder='results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for('upload_file'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    source = 'inputs/audio/'
    destination = 'inputs/saved/'
    out = 'results/saved/'

    for f in os.listdir(source):
        os.remove(os.path.join(source, f))
    for f in os.listdir(destination):
        os.remove(os.path.join(destination, f))
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main', name=filename))
    return '''
    <!doctype html>
    <title>Upload New File</title>
    <h1>Upload New File</h1>
    <body>
        <div>
        After you select the audio file, click upload to run the model
        </div>
        <br>
        <div>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
        </div>
    </body>
    '''


@app.route('/main', methods=['POST', 'GET'])
def main():
    for i in os.listdir('inputs/audio/'):
        if i.split('.')[-1] in able:
            file = i
            cli()
    for i in os.listdir('results/saved/'):
        if i.split('.')[-1] == 'txt':
            with open('results/saved/'+i, 'r') as f:
                content = f.read()
                print(content)
    return render_template("index3.html", content=content)
    return '''
    <!doctype html>
    <title>Your text output</title>
    <h1>Your text output</h1>
    <body>
        <div>
        {open(file_object).read()}
        </div>
        <br>

    </body>
    '''


if __name__ == '__main__':
    app.run(host="0.0.0.0")
    main()
