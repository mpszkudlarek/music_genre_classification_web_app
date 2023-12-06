import subprocess
import os
import librosa
import numpy as np
from pydub import AudioSegment
import keras
import tensorflow as tf


def convert_to_wav(audio_path):
    if os.path.splitext(audio_path)[1].lower() != '.wav':
        extension = os.path.splitext(audio_path)[0]
        subprocess.call(['ffmpeg', '-i', audio_path, extension + '.wav'])
        return extension + '.wav'
    return audio_path


def trim_audio(audio_path):
    audio_duration_ms = librosa.get_duration(filename=audio_path) * 1000  # Convert to milliseconds

    audio = AudioSegment.from_wav(audio_path)
    midpoint = int(audio_duration_ms / 2)

    start_trim = max(0, midpoint - 15000)  # Start 15 seconds before the midpoint
    end_trim = min(audio_duration_ms, midpoint + 15000)  # End 15 seconds after the midpoint

    trimmed_audio = audio[start_trim:end_trim]
    trimmed_audio.export(audio_path, format="wav")


def process_input(audio_file, sample_rate, track_duration, num_mfcc, n_fft, hop_length, num_segments):
    sample_per_track = sample_rate * track_duration
    samples_per_segment = int(sample_per_track / num_segments)
    signal, _ = librosa.load(audio_file, sr=sample_rate)

    for d in range(num_segments):
        start = samples_per_segment * d
        finish = start + samples_per_segment
        mfcc = librosa.feature.mfcc(y=signal[start:finish],
                                    sr=sample_rate,
                                    n_mfcc=num_mfcc,
                                    n_fft=n_fft,
                                    hop_length=hop_length).T
        return mfcc


def predict_genre(model, audio_file):
    genre_to_predict = audio_file[np.newaxis, ..., np.newaxis]
    predict = model.predict(genre_to_predict)
    return np.argmax(predict), model.predict(genre_to_predict)


def display_prediction(pred, prob, genre_dict):
    predicted_genre = genre_dict[pred]
    print("Predicted Genre:", predicted_genre)
    print(tf.greater(prob, .5))
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(prob)

    sorted_indices = np.argsort(prob)[::-1]
    for i in range(3):
        genre_index = sorted_indices[i]
        genre_name = genre_dict[genre_index]
        genre_probability = prob[genre_index]
        print(f"{genre_name}: {genre_probability:.2f}")


model = keras.models.load_model("git_modelv3.h5")
audio_path = "Garth Brooks- Friends In Low Places.mp3"
audio_path = convert_to_wav(audio_path)
trim_audio(audio_path)

audio_file = process_input(audio_path,
                           22050,
                           30,
                           13,
                           2048,
                           512,
                           10)

genre_dict = {0: "blues",
              1: "classical",
              2: "country",
              3: "disco",
              4: "hiphop",
              5: "jazz",
              6: "metal",
              7: "pop",
              8: "reggae",
              9: "rock"}

prediction, prob = predict_genre(model, audio_file)
display_prediction(prediction, prob[0], genre_dict)
