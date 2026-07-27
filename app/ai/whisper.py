import torch
import whisperx

from app.core.config import settings
import torch
import whisperx

from transformers import WhisperProcessor,WhisperForConditionalGeneration,pipeline
from whisperx.diarize import DiarizationPipeline
from huggingface_hub import login

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_whisper():
    login(settings.HF_TOKEN)
    
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    processor = WhisperProcessor.from_pretrained(settings.WHISPER_MODEL_PATH)

    model = WhisperForConditionalGeneration.from_pretrained(
        settings.WHISPER_MODEL_PATH,
        dtype=torch.float16 if DEVICE == "cuda" else torch.float32
    )
     
    model.to(DEVICE)
    model.eval()
    
    

    return {
        "model": model,
        "processor": processor,
    }
    