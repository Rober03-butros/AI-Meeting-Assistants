import torch
import whisperx

from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
)
from app.core.config import settings
from transformers import pipeline


def load_whisper():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(settings.WHISPER_MODEL_PATH)
    processor = WhisperProcessor.from_pretrained(settings.WHISPER_MODEL_PATH)

    model = WhisperForConditionalGeneration.from_pretrained(
        settings.WHISPER_MODEL_PATH,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
    )
     
    model.to(DEVICE)
    model.eval()

    asr = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device=0 if DEVICE == "cuda" else -1,
        chunk_length_s=30,
    )

    return {
        "model": model,
        "processor": processor,
        "pipeline": asr,
    }
    