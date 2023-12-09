import os
import subprocess
from pydub import AudioSegment
import sys
import keras
import numpy as np
import librosa

model = keras.models.load_model('git_modelv3.h5')


def check_extension(audio_path):
    _, ext = os.path.splitext(audio_path)
    ext = ext.lower()
    if ext not in ['.mp3', '.wav']:
        print("Unsupported file format. Only MP3 and WAV files are supported.")
        sys.exit(1)

    if ext != '.wav':
        extension = os.path.splitext(audio_path)[0]
        subprocess.call(['ffmpeg', '-i', audio_path, extension + '.wav'])
        return extension + '.wav'

    return audio_path


def split_audio(audio_path, temp_folder, segment_duration=30):
    wav_path = check_extension(audio_path)
    audio = AudioSegment.from_wav(wav_path)
    duration_ms = len(audio)
    segment_ms = segment_duration * 1000
    num_segments = int(duration_ms / segment_ms)

    audio_parts = []
    for i in range(num_segments):
        start, end = i * segment_ms, (i + 1) * segment_ms
        part = audio[start:end]
        part_file = os.path.join(temp_folder, f'part_{i}.wav')
        part.export(part_file, format='wav')
        audio_parts.append(part_file)

    return audio_parts


def extract_features(audio_file, sr=22050, duration=30, mfccs=13, fft=2048, hop=512, num_segments=10):
    total_samples = sr * duration
    samples_per_segment = int(total_samples / num_segments)
    signal, _ = librosa.load(audio_file, sr=sr)

    for d in range(num_segments):
        start, end = samples_per_segment * d, samples_per_segment * (d + 1)
        mfcc = librosa.feature.mfcc(
            y=signal[start:end],
            sr=sr,
            n_mfcc=mfccs,
            n_fft=fft,
            hop_length=hop).T
        return mfcc


def predict(audio_file):
    features = extract_features(audio_file)
    prediction_input = features[np.newaxis, ..., np.newaxis]
    probabilities = model.predict(prediction_input)
    return probabilities[0]
