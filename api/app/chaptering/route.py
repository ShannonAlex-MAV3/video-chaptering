from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from utils.aud_extractor import AudioExtractor
import os
from moviepy.audio.io import AudioFileClip
from media_analyzer.media_analyzer import analyze_video
import json
import tempfile

router = APIRouter()
# Get the absolute path of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))


@router.post("/vid-to-text")
async def vid_to_txt(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    video_path = os.path.join(base_dir, file.filename)
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Analyze the video
    chapters = analyze_video(video_path)

    # remove the temporary file after processing
    os.remove(video_path)

    return JSONResponse(content=chapters)
