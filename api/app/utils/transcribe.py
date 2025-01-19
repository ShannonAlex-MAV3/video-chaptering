import whisper
import numpy as np

class Transcribe:
    def __init__(self):
        self.model = whisper.load_model("base")
        
    def extract_text_from_audio(self, soundarray: np.ndarray) -> str:
        """Extract text from an audio numpy array."""
        audio = whisper.pad_or_trim(soundarray.flatten())
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        return result.text
    
    def extract_text_from_video(self, video: str) -> str:
        """Extract text from a video file."""
        result = self.model.transcribe(video)
        return result['text']
    
    def transcribe_from_video(self, video: str) -> dict[str, str | list]:
        """Transcribe from a video file. And extract the Segments"""
        result = self.model.transcribe(video)
        return result
