import tempfile
import os
import soundfile as sf

def transcribe_audio(audio_bytes, model):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path, language="en", fp16=False)
        transcript = result["text"].strip()
        # fallback to duration from audio if segments missing
        if "segments" in result and result["segments"]:
            duration = result["segments"][-1]["end"]
        else:
            duration = sf.info(tmp_path).duration
    except Exception as e:
        transcript = ""
        duration = 0.0
        print("Error during transcription:", e)
    finally:
        os.remove(tmp_path)

    return transcript, duration
