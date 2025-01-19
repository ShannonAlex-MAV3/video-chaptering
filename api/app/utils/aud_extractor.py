from moviepy import *
import numpy as np

class AudioExtractor:
    def __init__(self, vid_filename: str, aud_out_filename: str):
        self.vid_filename = vid_filename
        self.aud_out_filename = aud_out_filename
        self.audio = None

    def extract_audio(self) -> AudioFileClip:
        try:
            self.audio = AudioFileClip(self.vid_filename)
            print("Audio extraction successful!")
            return self.audio
        except Exception as e:
            raise RuntimeError(f"Error extracting audio: {e}")
        finally:
            if self.audio:
                self.audio.close()

    def to_soundarray(self, sampling_rate: int) -> np.ndarray:
        if self.audio is None:
            raise ValueError("Audio has not been extracted.")
        audio_array = self.audio.to_soundarray(fps=sampling_rate)
        self.audio_array = np.mean(audio_array, axis=1)
        return self.audio_array

    def save_audio(self) -> None:
        if self.audio is None:
            raise ValueError("Please extract audio before saving.")
        self.audio.write_audiofile(self.aud_out_filename)
        self.audio.close()
