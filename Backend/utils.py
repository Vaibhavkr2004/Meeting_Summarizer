import os
from moviepy.editor import VideoFileClip
from better_profanity import profanity

# Initialize profanity filter
profanity.load_censor_words()

def extract_audio_from_video(video_path):
    """
    Converts a video file into a .wav audio file.
    Returns the audio file path.
    """
    print(f"Extracting audio from video: {video_path}")
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

def contains_profanity(text):
    """
    Checks if the transcript contains profanity.
    Returns True/False.
    """
    return profanity.contains_profanity(text)
