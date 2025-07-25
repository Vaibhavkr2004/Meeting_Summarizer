from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from transcriber import transcribe_audio
from summarizer import generate_summary_and_actions
from utils import extract_audio_from_video, contains_profanity
from flask_cors import CORS
import traceback

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'mkv', 'mov'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return '✅ Flask backend is running'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            print(f"📁 File saved to: {filepath}")

            # Extract audio from video if needed
            if filename.lower().endswith(('.mp4', '.mkv', '.mov')):
                print("🎥 Extracting audio from video ...")
                audio_path = extract_audio_from_video(filepath)
            else:
                audio_path = filepath

            print(f"🎙️ Transcribing: {audio_path}")
            transcript, speakers = transcribe_audio(audio_path)

            print("🧠 Generating summary and actions ...")
            summary, actions = generate_summary_and_actions(transcript)

            print("🧼 Checking for profanity ...")
            profane = contains_profanity(transcript)

            return jsonify({
                'transcript': transcript,
                'speakers': speakers,
                'summary': summary,
                'action_items': actions,
                'contains_profanity': profane
            })

        return jsonify({'error': 'Invalid file format'}), 400

    except Exception as e:
        print("❌ An error occurred during file processing:")
        traceback.print_exc()  # Shows full error in terminal
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
