import torch
from TTS.api import TTS
from fastapi import FastAPI, status
from pydantic import BaseModel

class ConversionRequest(BaseModel):
    text: str
    fileName: str

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/de/css10/vits-neon").to(device)

@app.post("/convert")
def convert(request: ConversionRequest, status_code=status.HTTP_204_NO_CONTENT):
    tts.tts_to_file(
        text=request.text,
        file_path=f"out/{request.fileName}.wav"
    )
    return