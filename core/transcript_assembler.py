from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TranscriptChunk:
    """Data for a single transcribed chunk."""

    index: int
    start: float
    end: float
    text: str
    word_timestamps: List[Dict[str, float]] | None = None


class TranscriptAssembler:
    """Reassemble ordered transcript chunks and adjust timestamps."""

    def assemble(self, chunks: List[TranscriptChunk]) -> Dict[str, Any]:
        ordered = sorted(chunks, key=lambda c: c.index)
        text_parts: List[str] = []
        words: List[Dict[str, float]] = []

        for chunk in ordered:
            text_parts.append(chunk.text)
            for wt in chunk.word_timestamps or []:
                words.append(
                    {
                        **wt,
                        "start": wt["start"] + chunk.start,
                        "end": wt["end"] + chunk.start,
                    }
                )

        return {
            "text": " ".join(t.strip() for t in text_parts).strip(),
            "words": words,
        }


__all__ = ["TranscriptAssembler", "TranscriptChunk"]
