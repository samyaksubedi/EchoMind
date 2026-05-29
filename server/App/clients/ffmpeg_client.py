# clients/ffmpeg_client.py
import subprocess
import uuid
import os


def extract_audio_from_video(video_path: str) -> str:
    # generate unique output path internally
    output_path = f"/tmp/echomind/{uuid.uuid4()}.mp3"
    os.makedirs("/tmp/echomind", exist_ok=True)

    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", output_path])
    return output_path  # caller gets back the audio path
