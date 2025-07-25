import whisper
import os

# ✅ TEMPORARY FIX: Add FFmpeg path explicitly to avoid FileNotFoundError
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-2025-07-23-git-829680f96a-full_build\bin"

# Load the Whisper model (you can also use "small", "medium", or "large")
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    print(f"🎙️ Transcribing: {audio_path} ...")

    result = model.transcribe(audio_path, verbose=False)
    text = result['text']

    # Placeholder since Whisper doesn't provide speakers by default
    speakers = ["Speaker 1"]

    return text.strip(), speakers
