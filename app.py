import os
import uuid
import numpy as np
import shutil
from werkzeug.utils import secure_filename
from support_functions import split_audio, predict, check_file_signature, get_gpu_info, get_system_performance
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

genre_labels = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    predicted_genres = None

    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part in the request")
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']

        if file.filename == '':
            print("No selected file")
            return jsonify({"error": "No selected file"}), 400

        if file:
            print("File received")
            print("before prediction")
            print(get_gpu_info())
            cpu_before, ram_before, disk_usage_before = get_system_performance()
            print(f"CPU usage before prediction: {cpu_before}%")
            print(f"RAM usage before prediction: {ram_before}%")
            print(f"Disk usage before prediction: {disk_usage_before}%")
            temp_id = str(uuid.uuid4())
            print(f"Temp id: {temp_id}")
            temp_folder = os.path.join('tmp_directory', temp_id)
            os.makedirs(temp_folder, exist_ok=True)
            audio_file_path = os.path.join(temp_folder, file.filename)
            file.save(audio_file_path)

            audio_parts = split_audio(audio_file_path, temp_folder)
            genre_probabilities = np.zeros(len(genre_labels))

            for part in audio_parts:
                genre_probabilities += predict(part)

            average_probabilities = genre_probabilities / len(audio_parts)

            top_genres = np.argsort(average_probabilities)[::-1][:3]
            predicted_genres = [{"genre": genre_labels.get(index, "Unknown"), "probability": average_probabilities[index]} for index in top_genres]

            print(get_gpu_info())
            print("after prediction")
            cpu_after, ram_after, disk_usage_after = get_system_performance()
            print(f"CPU usage after prediction: {cpu_after}%")
            print(f"RAM usage after prediction: {ram_after}%")
            print(f"Disk usage after prediction: {disk_usage_after}%")
            print('temp_folder', temp_folder)
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

        else:
            print("Temp folder does not exist.")

    return render_template('prediction.html', predicted_genres=predicted_genres)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html')


if __name__ == '__main__':
    app.run(debug=True)
