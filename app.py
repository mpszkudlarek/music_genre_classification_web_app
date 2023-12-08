import os
import uuid
import numpy as np
import shutil
from support_functions import split_audio, predict
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

genre_labels = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    predicted_genres = None

    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part in the request")

            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            print("No selected file")
            return redirect(request.url)

        if file:
            print('tutaj file')
            temp_id = str(uuid.uuid4())
            temp_folder = os.path.join('tmp_directory', temp_id)
            os.makedirs(temp_folder, exist_ok=True)
            audio_file_path = os.path.join(temp_folder, file.filename)
            file.save(audio_file_path)

            audio_parts, _ = split_audio(audio_file_path)
            genre_probabilities = np.zeros(len(genre_labels))

            for part in audio_parts:
                genre_probabilities += predict(part)

            average_probabilities = genre_probabilities / len(audio_parts)

            top_genres = np.argsort(average_probabilities)[::-1][:3]
            predicted_genres = [{"genre": genre_labels.get(index, "Unknown"), "probability": average_probabilities[index]} for index in top_genres]
            print(predicted_genres)
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

    return render_template('prediction.html', predicted_genres=predicted_genres)


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
