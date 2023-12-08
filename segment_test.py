import os
import librosa
from pydub import AudioSegment
import subprocess


def convert_to_wav(audio_path):
    if os.path.splitext(audio_path)[1].lower() != '.wav':
        extension = os.path.splitext(audio_path)[0]
        subprocess.call(['ffmpeg', '-i', audio_path, extension + '.wav'])
        return extension + '.wav'
    return audio_path


def split_audio_into_segments(audio_path, segment_length=30, output_folder='segments'):
    audio_path = convert_to_wav(audio_path)
    audio = AudioSegment.from_wav(audio_path)
    audio_duration_ms = len(audio)
    segment_length_ms = segment_length * 1000
    num_segments = int(audio_duration_ms / segment_length_ms)

    for i in range(num_segments):
        start_ms = i * segment_length_ms
        end_ms = start_ms + segment_length_ms
        segment = audio[start_ms:end_ms]
        segment.export(os.path.join(output_folder, f'segment_{i}.wav'), format='wav')


audio_path = 'track_to_test/BTS - DYNAMITE.mp3'
split_audio_into_segments(audio_path)
