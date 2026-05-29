# services/media_processing_service.py
from app.clients.whisper_client import transcribe
from app.clients.qdrant_client import embed_and_store
from app.utils.audio_util import chunk_segments
from app.utils.pdf_util import load_and_chunk_pdf
from clients.ytdlp_client import download_youtube_audio
from clients.ffmpeg_client import extract_audio_from_video


def process_media(conversation_id, file_path, source_type):
    if source_type == "youtube":
        audio_path = download_youtube_audio(
            file_path
        )  # extra step -Here file path is youtube Link : )
        _process_audio_pipeline(conversation_id, audio_path)

    elif source_type == "video":
        audio_path = extract_audio_from_video(file_path)  # extra step
        _process_audio_pipeline(conversation_id, audio_path)

    elif source_type == "audio":
        _process_audio_pipeline(conversation_id, file_path)  # skip extraction

    elif source_type == "pdf":
        _process_pdf_pipeline(conversation_id, file_path)  # different pipeline


def _process_audio_pipeline(conversation_id, audio_path):
    # same for youtube/video/audio
    segments = transcribe(audio_path)  # whisper_client
    chunks = chunk_segments(segments)  # audio_utils
    embed_and_store(chunks, conversation_id)  # qdrant


def _process_pdf_pipeline(conversation_id, file_path):
    # different pipeline
    chunks = load_and_chunk_pdf(file_path=file_path)
    embed_and_store(chunks, conversation_id)  # qdrant
