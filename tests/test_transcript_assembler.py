import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.transcript_assembler import TranscriptAssembler, TranscriptChunk


def test_transcript_assembler_orders_and_adjusts():
    chunks = [
        TranscriptChunk(
            index=1,
            start=5.0,
            end=10.0,
            text="world",
            word_timestamps=[{"word": "world", "start": 0.0, "end": 1.0}],
        ),
        TranscriptChunk(
            index=0,
            start=0.0,
            end=5.0,
            text="hello",
            word_timestamps=[{"word": "hello", "start": 0.0, "end": 1.0}],
        ),
    ]
    assembler = TranscriptAssembler()
    result = assembler.assemble(chunks)

    assert result["text"] == "hello world"
    assert result["words"] == [
        {"word": "hello", "start": 0.0, "end": 1.0},
        {"word": "world", "start": 5.0, "end": 6.0},
    ]
