# clients/ytdlp_client.py
import yt_dlp
import uuid
import os


def download_youtube_audio(url: str) -> str:
    # generate unique output path internally
    output_path = f"/tmp/echomind/{uuid.uuid4()}.mp3"
    os.makedirs("/tmp/echomind", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path
