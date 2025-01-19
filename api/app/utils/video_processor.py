from typing import List, Dict, Tuple
import requests
import datetime
import json
from utils.transcribe import Transcribe
import google.generativeai as genai
import os

class VideoProcessor:

    def transcribe_video(self, video: str) -> List[Dict]:
        """
        Transcribe video using Google Gemini API and return segments with timestamps.
        """
        txtExtractor: Transcribe = Transcribe()
        transcription: dict[str, str |
                            list] = txtExtractor.transcribe_from_video(video)
        return transcription["segments"]

    def analyze_content(self, transcript) -> List[Dict]:
        """
        Analyze content and create chapters using Google Gemini API.
        """

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        gemini_model = os.getenv("GEMINI_MODEL")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(
            model_name=gemini_model,
            system_instruction=self.system_instruction(),
        )
        response = model.generate_content(transcript)

        # Remove triple backticks and any leading/trailing whitespace
        raw_content = response.text
        raw_content = raw_content.strip()
        if raw_content.startswith("```") and raw_content.endswith("```"):
            raw_content = raw_content[3:-3].strip()

        # Handle case where content starts with "json\n"
        if raw_content.startswith("json\n"):
            raw_content = raw_content[5:]

        # Parse the cleaned JSON string
        try:
            json_object = json.loads(raw_content)
            return json_object
        except json.JSONDecodeError as e:
            print("Error: Could not parse the content as JSON.")
            print("Raw Content:", raw_content)
            return None

    def format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to HH:MM:SS format.
        """
        return str(datetime.timedelta(seconds=int(seconds)))

    def create_timestamped_transcript(self, segments: List[Dict]) -> str:
        """
        Create a formatted transcript with timestamps.
        """
        transcript = []
        for segment in segments:
            start_time = self.format_timestamp(segment['start'])
            text = segment['text']
            transcript.append(f"[{start_time}] {text}")
        return "\n".join(transcript)

    def system_instruction(self) -> str:
        prompt = f"""
        You are a video transcription analyzer. Your task is to break down the following video transcription into structured chapters.

        Go thorugh the transcription and IDENTIFY KEY TOPICS or CHANGES in SUBJECT MATTER. Split the transcription into chapters based on these topics.
        
        Rules for processing:
        1. Keep the exact wording from the transcription in the "content" field
        2. Do not paraphrase or modify the original text
        3. Split chapters based on clear topic changes or natural pauses
        4. Each chapter must contain direct quotes from the transcription
        5. **You MUST respond with a valid JSON output only. Do NOT output any other text or explanations.**

        Required JSON structure:
        {{
        "chapters": [
            {{
            "chapterNumber": [number],
            "title": [brief descriptive title, max 8 words],
            "content": [exact text from transcription for this section],
            "startTime": [timestamp]
            "endTime": [timestamp]
            }}
        ],
        "metadata": {{
            "totalChapters": [number],
            "mainTopics": [array of key topics covered]
        }}
        }}
        
        **Your Response MUST be in JSON format.**

        """

        return prompt
