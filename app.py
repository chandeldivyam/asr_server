import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisperx
import torch
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from environment variables
HF_TOKEN = os.getenv("HF_TOKEN")

# Global variables to store loaded models
whisper_model = None
diarize_model = None

@app.on_event("startup")
async def load_models():
    global whisper_model, diarize_model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if torch.cuda.is_available() else "int8"

    whisper_model = whisperx.load_model("medium", device, compute_type=compute_type)
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    try:
        # Load audio
        audio = whisperx.load_audio(file.filename)

        # Transcribe with WhisperX
        result = whisper_model.transcribe(audio, batch_size=48, language="en")

        # Perform diarization
        diarize_segments = diarize_model(audio)

        # Assign speakers to words
        result = whisperx.assign_word_speakers(diarize_segments, result)

        # Clean up the temporary file
        os.remove(file.filename)

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
