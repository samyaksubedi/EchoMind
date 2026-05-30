from faster_whisper import WhisperModel
from app.config import settings


def transcribe(audio_path: str) -> list[dict]:
    if settings.WHISPER_MODE == "local":
        return _transcribe_local(audio_path)
    else:
        return _transcribe_api(audio_path)


def _transcribe_local(audio_path: str) -> list[dict]:
    model = WhisperModel("medium", device="cuda")
    segments, _ = model.transcribe(audio_path)
    return [{"start": s.start, "end": s.end, "text": s.text} for s in segments]


def _transcribe_api(audio_path: str) -> list[dict]:
    from openai import OpenAI

    client = OpenAI()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    return [{"start": s.start, "end": s.end, "text": s.text} for s in result.segments]
