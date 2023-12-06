from flask import Flask, render_template, request
import smtplib
from datetime import datetime
import tensorflow as tf
import keras
import librosa
import numpy as np
import math
from pydub import AudioSegment

model = keras.models.load_model("git_modelv3.h5")

app = Flask(__name__)


@app.route("/")
def homepage():
    title = "MGC"
    return render_template('homepage.html', title=title)


@app.route("/prediction", methods=["POST"])
def prediction():


@app.route("/about")
def about():
    title = "MGC | About"
    return render_template('about.html', title=title)


@app.route("/project")
def project():
    title = "MGC | Project"
    return render_template('project.html', title=title)
