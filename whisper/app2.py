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
                
from flask_restful import Resource

class GetFile(Resource):
    def get(self, filename):
        return {
            "directory": 'results/subbed_vids/',
            "filename": filename
        }

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


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


@app.route('/main', methods=['POST', 'GET'])
def main():
    for i in os.listdir('inputs/audio/'):
        if i.split('.')[-1] in able:
            file = i
            cli()
    for i in os.listdir('results/saved/'):
        if i.split('.')[-1] == 'txt':
            with open('results/saved/'+i, 'r') as f:
                return get(f)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
    main()
