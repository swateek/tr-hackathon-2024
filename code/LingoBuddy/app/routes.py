"""routes.py"""

from flask import current_app as app, render_template, request, jsonify
import os
import json
import chromadb
from audio_translation import (
    extract_audio_from_video,
    generate_new_audio,
    overlay_audio_on_video,
    save_transcriptions_to_txt,
)
import time
import boto3
import urllib

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
local_embeddings = []
VIDEO_DIR = "../../translated_video"
TRANSCRIPTION_TXT_DIR = "../../transcription"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection("pdf_embeddings")

AWS_REGION = "us-west-2"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_SESSION_TOKEN = ""
S3_BUCKET = "tr-hackathon"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    aws_session_token=AWS_SESSION_TOKEN,
)

transcribe_client = boto3.client(
    "transcribe",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    aws_session_token=AWS_SESSION_TOKEN,
)

translate_client = boto3.client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    aws_session_token=AWS_SESSION_TOKEN,
)

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    aws_session_token=AWS_SESSION_TOKEN,
)

system_prompt = "Give a text of transcribed text of a video, generate a concise summary of 80-120 words. \
Ensure to not miss out on any important points. \
The input text can be in any language, and the summary has to be returned in the same language. \
Return the response containing only the summary."


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """allowed_file"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """index"""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    """upload_audio"""
    audio_file = request.files["file"]
    if not audio_file:
        return jsonify({"error": "No file uploaded"}), 400

    file_name = audio_file.filename

    # Upload the file to S3 first
    s3_key = f"videos/{str(time.time())}-{file_name}"
    s3_client.upload_fileobj(audio_file, S3_BUCKET, s3_key)
    file_url = f"s3://{S3_BUCKET}/{s3_key}"

    # Define language codes
    language = request.form["language"]
    language_codes = {
        "hindi": "hi",
        "tamil": "ta",
        "telugu": "te",
        "assamese": "as",
        "gujarati": "gu",
        "bengali": "bn",
        "kannada": "kn",
        "malayalam": "ml",
        "marathi": "mr",
        "nepali": "ne",
    }

    # Define paths for local processing
    video_path = "app/static/videos/source_video/genai.mp4"
    audio_path = "app/static/audio/audio.wav"
    new_audio_path = "app/static/translated_audio/new_audio.mp3"
    final_video_path = "app/static/videos/translated_video/translated_video.mp4"
    transcription_txt_path = "app/static/transcription/transcription.txt"
    translation_txt_path = "app/static/translation/translation.txt"
    summary_txt_path = "app/static/summary/summary.txt"

    # Ensure directories exist
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(new_audio_path), exist_ok=True)
    os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
    os.makedirs(os.path.dirname(transcription_txt_path), exist_ok=True)
    os.makedirs(os.path.dirname(translation_txt_path), exist_ok=True)
    os.makedirs(os.path.dirname(summary_txt_path), exist_ok=True)

    # Process the video locally in parallel with the transcription job
    extract_audio_from_video(video_path, audio_path)

    # Start AWS transcription job
    job_name = f"transcription-{int(time.time())}"
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": file_url},
            MediaFormat="mp4",
            LanguageCode="en-US",
            OutputBucketName=S3_BUCKET,
        )

        # Wait for transcription job to complete
        while True:
            response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]
            if status in ["COMPLETED", "FAILED"]:
                break
            time.sleep(5)

        # Check if transcription was successful
        if status == "COMPLETED":
            transcript_url = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            response = urllib.request.urlopen(transcript_url)
            data = json.loads(response.read())
            transcription_text = data["results"]["transcripts"][0]["transcript"]
        else:
            return jsonify({"error": "Transcription failed"}), 500

        translated_text = translate_client.translate_text(
            Text=transcription_text,
            SourceLanguageCode="en",
            TargetLanguageCode=language_codes[language],
        ).get("TranslatedText")

        payload = {
            "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": translated_text}],
                    }
                ],
                "system": system_prompt,
            },
        }
        response = bedrock_runtime.invoke_model(
            modelId=payload["modelId"], body=json.dumps(payload["body"]).encode("utf-8")
        )
        response_body = json.loads(response.get("body").read()).get("content")[0][
            "text"
        ]

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Proceed with the local video processing
    generate_new_audio(translated_text, new_audio_path, language_codes[language])
    save_transcriptions_to_txt(transcription_text, transcription_txt_path)
    save_transcriptions_to_txt(translated_text, translation_txt_path)
    save_transcriptions_to_txt(response_body, summary_txt_path)

    # Overlay the new translated audio onto the video
    overlay_audio_on_video(video_path, new_audio_path, final_video_path)

    # Return both the transcription and the translated text
    return jsonify(
        {
            "transcribed_text": transcription_text,
            "translated_text": translated_text,
            "summary": response_body,
        }
    )
