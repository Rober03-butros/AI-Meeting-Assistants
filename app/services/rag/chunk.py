from __future__ import annotations
from sqlalchemy.orm import Session

from dataclasses import dataclass

from app.models.chunk import MeetingChunk


@dataclass
class TranscriptChunk:
    text: str
    start: float
    end: float


def create_chunks(segments: list[dict],max_words: int = 150,min_words: int = 50,overlap_ratio: float = 0.2):

    chunks: list[TranscriptChunk] = []

    current_chunk: list[dict] = []
    current_words = 0

    start_time = 0.0
    end_time = 0.0

    for segment in segments:

        text = segment["text"].strip()
        word_count = len(text.split())

        if not current_chunk:
            start_time = segment["start"]

        if current_words + word_count <= max_words:

            current_chunk.append(segment)
            current_words += word_count
            end_time = segment["end"]

        else:

            if current_words >= min_words:

                chunks.append(
                    TranscriptChunk(
                        text=" ".join(
                            s["text"].strip()
                            for s in current_chunk
                        ),
                        start=start_time,
                        end=end_time,
                    )
                )

                overlap_count = max(
                    1,
                    int(len(current_chunk) * overlap_ratio),
                )

                overlap_count = min(
                    overlap_count,
                    len(current_chunk),
                )

                current_chunk = current_chunk[-overlap_count:]

                current_words = sum(
                    len(s["text"].split())
                    for s in current_chunk
                )

                start_time = current_chunk[0]["start"]

            current_chunk.append(segment)
            current_words += word_count
            end_time = segment["end"]

    if current_chunk:

        chunks.append(
            TranscriptChunk(
                text=" ".join(
                    s["text"].strip()
                    for s in current_chunk
                ),
                start=start_time,
                end=end_time,
            )
        )

    return chunks



def save_chunks(db: Session,meeting_id: int,chunks: list[TranscriptChunk]):

    for index, chunk in enumerate(chunks):

        db_chunk = MeetingChunk(

            meeting_id=meeting_id,

            chunk_index=index,

            content=chunk.text,

            start_time=chunk.start,

            end_time=chunk.end,
        )

        db.add(db_chunk)

    db.commit()