import os

import torch
from TTS.api import TTS
from fastapi import FastAPI, status
from pydantic import BaseModel
from starlette.responses import JSONResponse
from pydub import AudioSegment


class ConversionRequest(BaseModel):
    text: str
    fileName: str


os.makedirs("./out", exist_ok=True)

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/de/css10/vits-neon").to(device)


@app.post("/convert")
def convert(request: ConversionRequest, status_code=status.HTTP_204_NO_CONTENT):
    audio_path = f"./out/{request.fileName}.wav"
    tts.tts_to_file(
        text=request.text,
        file_path=audio_path,
    )

    sound = AudioSegment.from_file(audio_path)
    sound = sound.set_frame_rate(8000)
    sound.export(audio_path, format="wav")

    return JSONResponse(content={})


@app.get("/healthcheck")
def healthcheck(status_code=status.HTTP_200_OK):
    return JSONResponse(content={})
