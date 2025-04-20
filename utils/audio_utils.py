import whisper
import tempfile
import os
import soundfile as sf

model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path, language="en")
        transcript = result["text"].strip()
        duration = result["segments"][-1]["end"]
    except Exception as e:
        transcript = ""
        duration = 0.0
        print("Error during transcription:", e)
    finally:
        os.remove(tmp_path)

    return transcript, duration
