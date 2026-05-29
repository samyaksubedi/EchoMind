def chunk_segments(
    segments: list[dict], chunk_size: int = 5, overlap: int = 1
) -> list[dict]:
    chunks = []
    i = 0
    while i < len(segments):
        # take chunk_size segments
        group = segments[i : i + chunk_size]

        # merge their text
        text = " ".join([s["text"] for s in group])

        chunks.append(
            {
                "text": text,
                "startTime": group[0]["start"],  # start of first segment
                "endTime": group[-1]["end"],  # end of last segment
            }
        )

        # move forward by (chunk_size - overlap)
        # overlap=1 means last segment of this chunk = first of next
        i += chunk_size - overlap

    return chunks
