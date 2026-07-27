# import torch
# import whisperx

# from transformers import (
#     WhisperProcessor,
#     WhisperForConditionalGeneration,
# )


# from app.core.config import settings


# def load_whisper():

#     processor = WhisperProcessor.from_pretrained(
#         settings.WHISPER_MODEL_PATH
#     )

#     model = WhisperForConditionalGeneration.from_pretrained(
#         settings.WHISPER_MODEL_PATH,
#         torch_dtype=(
#             torch.float16
#             if DEVICE == "cuda"
#             else torch.float32
#         ),
#     )

#     model.to(DEVICE)
#     model.eval()

#     vad_model = load_silero_vad()

#     align_model, metadata = whisperx.load_align_model(
#         language_code="ar",
#         device=DEVICE,
#     )

#     diarization = DiarizationPipeline(
#         device=DEVICE,
#     )

#     forced_decoder_ids = processor.get_decoder_prompt_ids(
#         language="ar",
#         task="transcribe",
#     )

#     return {

#         "model": model,

#         "processor": processor,

#         "vad": vad_model,

#         "align_model": align_model,

#         "align_metadata": metadata,

#         "diarization": diarization,

#         "forced_decoder_ids": forced_decoder_ids,

#         "device": DEVICE,

#     }