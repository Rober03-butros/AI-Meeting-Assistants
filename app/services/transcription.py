# import threading
# from app.services.rag.embedding import run_embedding_pipeline

# from sqlalchemy.orm import Session
# from app.ai.whisper import DEVICE
# from app.core.database import SessionLocal
# from app.models.meeting import Meeting
# from app.core.Enum import TranscriptStatus
# from app.services.rag.chunk import create_chunks, save_chunks

# from app.ai.model_manager import model_manager
# from silero_vad import load_silero_vad,read_audio,get_speech_timestamps
# import torch
# import whisperx

# from whisperx.diarize import DiarizationPipeline



# SAMPLE_RATE = 16000
# vad_model = load_silero_vad()

# def split_audio_vad(audio_path):
#     audio = read_audio(audio_path, sampling_rate=SAMPLE_RATE)
#     speech = get_speech_timestamps(
#         audio,
#         vad_model,
#         sampling_rate=SAMPLE_RATE,
#         threshold=0.5,
#         min_speech_duration_ms=250,
#         min_silence_duration_ms=400,
#         return_seconds=False,
#     )
#     chunks = []
#     for seg in speech:
#         start = seg["start"]
#         end = seg["end"]
#         chunks.append(
#             {
#                 "audio": audio[start:end].numpy(),
#                 "start": start / SAMPLE_RATE,
#                 "end": end / SAMPLE_RATE,
#             }
#         )
#     return chunks


# def run_transcription(meeting_id: int):

#     db: Session = SessionLocal()

#     meeting = None


#     try:


#         meeting = ( 
#             db.query(Meeting)
#             .filter(
#                 Meeting.id == meeting_id
#             )
#             .first()
#         )


#         if not meeting:
#             return


#         meeting.transcript_status = TranscriptStatus.PROCESSING

#         db.commit()

#         audio_path = meeting.audio.path

#         whisper = model_manager.whisper
                
#         if whisper is None:
#             raise Exception(
#                 "Whisper model is not loaded"
#             )
        
#         model = whisper['model']
#         processor = whisper['processor']
        
#         forced_decoder_ids = processor.get_decoder_prompt_ids(
#             language="ar",
#             task="transcribe"
#             )
            
#         all_segments = []
#         chunks = split_audio_vad(audio_path)
#         for chunk in chunks:
#             if len(chunk["audio"]) < SAMPLE_RATE:
#                 continue

#             inputs = processor(chunk["audio"],sampling_rate=16000,return_tensors="pt")
#             input_features = inputs.input_features.to(DEVICE,dtype=model.dtype,)
#             with torch.no_grad():
#                 predicted_ids = model.generate(
#                     input_features,
#                     forced_decoder_ids=forced_decoder_ids,
#                     num_beams=5,
#                     do_sample=False,
#                     temperature=0.0,
#                     max_new_tokens=225,
#                     no_repeat_ngram_size=3,
#                 )
#             text = processor.batch_decode(predicted_ids,skip_special_tokens=True,)[0]
#             if not text.strip():
#                 continue
#             all_segments.append(
#                 {
#                     "start": chunk["start"],
#                     "end": chunk["end"],
#                     "text": text,
#                 }
#             )    
            
            
#         segments = []

#         for s in all_segments:
#             segments.append({"start": s["start"],
#                             "end": s["end"],
#                             "text": s["text"],})
        
#         audio = whisperx.load_audio(audio_path)

#         model_a, metadata = whisperx.load_align_model(device=DEVICE,language_code="ar",)

#         result = whisperx.align(
#             segments,
#             model_a,
#             metadata,
#             audio,
#             DEVICE,
#         ) 
        
#         diarize_model = DiarizationPipeline(device=DEVICE)
#         diarize_segments = diarize_model(audio_path)
#         result = whisperx.assign_word_speakers(diarize_segments,result)

#         chunks = create_chunks(result["segments"])

#         save_chunks(
#             db=db,
#             meeting_id=meeting.id,
#             chunks=chunks,
#         )
        
#         transcrip = ''
#         for segment in result["segments"]:
#             speaker = segment.get("speaker","UNKNOWN")
#             transcrip += '\n'+f"[{segment['start']:.2f} -> {segment['end']:.2f}] " + f"{speaker}: {segment['text']}"


#         meeting.transcript = transcrip


        # meeting.transcript_status = TranscriptStatus.COMPLETED
        # meeting.embedding_status = TranscriptStatus.PROCESSING

        # threading.Thread(

        #     target=run_embedding_pipeline,

        #     args=(meeting.id,),

        #     daemon=True,

        # ).start()



#         db.commit()



#     except Exception as e:

#         if meeting:

#             meeting.transcript_status = TranscriptStatus.FAILED

#             db.commit()



#     finally:

#         db.close()





# ===== just because whisper doesn't work in rober's laptop
def run_transcription(meeting_id: int):
    pass