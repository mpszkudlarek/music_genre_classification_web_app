import os
import subprocess
import librosa
from matplotlib import pyplot as plt
from pydub import AudioSegment
import keras
import numpy as np
import uuid
import shutil
import sys

genre_labels = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}
output_directory = 'charts_genres'
chart_filename = 'test.png'
output_filename = 'Kendrick Lamar - Money Trees.txt'
correct_genre_index = 4
model = keras.models.load_model('git_modelv3.h5')

audio_file_path = 'track_to_test/Kendrick Lamar - Money Trees.mp3'
segment_duration = 30
overlap = 15


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


def split_audio(audio_path, segment_duration=30, overlap=15):
    temp_id = str(uuid.uuid4())
    temp_folder = os.path.join('tmp_directory', temp_id)
    os.makedirs(temp_folder, exist_ok=True)

    wav_path = check_extension(audio_path)
    audio = AudioSegment.from_wav(wav_path)
    duration_ms = len(audio)
    segment_ms = segment_duration * 1000
    overlap_ms = overlap * 1000
    num_segments = int(duration_ms / (segment_ms - overlap_ms))

    audio_parts = []
    for i in range(num_segments):
        start = i * (segment_ms - overlap_ms)
        end = start + segment_ms
        part = audio[start:end]
        part_file = os.path.join(temp_folder, f'part_{i}.wav')
        part.export(part_file, format='wav')
        audio_parts.append(part_file)

    return audio_parts, temp_folder


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


audio_parts, temp_directory = split_audio(audio_file_path, segment_duration, overlap)

genre_probabilities_list = []

for i, part in enumerate(audio_parts):
    genre_probabilities = predict(part)
    genre_probabilities_list.append(genre_probabilities[correct_genre_index])

    print(f"Segment {i + 1} Prediction:")
    genre = genre_labels.get(correct_genre_index, "Unknown")
    probability = genre_probabilities[correct_genre_index]
    print(f'{genre}: {probability:.8f}')
    print()

segment_numbers = list(range(1, len(audio_parts) + 1))

os.makedirs(output_directory, exist_ok=True)
chart_filename = os.path.join(output_directory, chart_filename)
plt.savefig(chart_filename)

output_text = []
for i, probability in enumerate(genre_probabilities_list):
    output_text.append(f"Segment {i + 1} Prediction:")
    genre = genre_labels.get(correct_genre_index, "Unknown")
    output_text.append(f'{genre}: {probability}')
    output_text.append("\n")

output_filename = os.path.join(output_directory, output_filename)
with open(output_filename, 'w') as text_file:
    text_file.write('\n'.join(output_text))

if os.path.exists(temp_directory):
    shutil.rmtree(temp_directory)
