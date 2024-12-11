"""audio_translation.py"""

from deep_translator import GoogleTranslator
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import speech_recognition as sr
import os
import shutil
import textwrap


def extract_audio_from_video(video_path, audio_path):
    """extract_audio_from_video"""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()


def transcribe_audio(audio_path):
    """transcribe_audio"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    transcription = recognizer.recognize_google(audio)
    return transcription


"""def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        # Using pocketsphinx for offline recognition
        transcription = recognizer.recognize_sphinx(audio)
    except sr.UnknownValueError:
        transcription = "Pocketsphinx could not understand the audio"
    except sr.RequestError as e:
        transcription = f"Pocketsphinx request error: {e}"
    return transcription"""


def translate_text_to_tamil(text, language):
    """translate_text_to_tamil"""
    translator = GoogleTranslator(source="auto", target=language)
    translated_text = translator.translate(text)
    return translated_text


def generate_new_audio(text, output_path, language):
    """generate_new_audio"""
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)


def overlay_audio_on_video(video_path, audio_path, output_path):
    """overlay_audio_on_video"""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video.close()
    audio.close()


def save_transcriptions_to_txt(original_transcription, output_path):
    """save_transcriptions_to_txt"""
    with open(output_path, "w", encoding="utf-8") as f:
        wrapped_text = textwrap.fill(original_transcription, width=80)
        f.write(wrapped_text + "\n")


def clear_folders(folders):
    """clear_folders"""
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)


youtube_url = "https://www.youtube.com/watch?v=Sn-jsiJOKA8&t=4s"
