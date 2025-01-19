import datetime
import requests
import os
import json
from typing import List, Dict, Any, Set
from utils.video_processor import VideoProcessor

ollama_url = os.getenv("OLLAMA_API")
ollama_model = os.getenv("OLLAMA_MODEL")
headers = {"Content-Type": "application/json"}

# using the VideoProcessor class and whisper API and gemini API (flash model) to process the video and generate chapters
def analyze_video(video):
    """
    Process a video file and return the transcript and chapters.
    """
    processor = VideoProcessor()

    # Transcribe video
    print("Transcribing video...")
    segments = processor.transcribe_video(video)

    # Create timestamped transcript
    print("Creating transcript...")
    transcript = processor.create_timestamped_transcript(segments)

    # Analyze content and create chapters
    print("Analyzing content and creating chapters...")
    chapters = processor.analyze_content(transcript)

    return {
        "transcript": transcript,
        "chapters": chapters
    }






# Generate chapter timestamps and summaries using Whisper segments and gemma2:2b model
# below is old code

def generate_chapters(transcription):
    """Generate chapter timestamps and summaries using Whisper segments"""

    # Detect chapter boundaries
    chapter_boundaries = chapter_breakdown(transcription["text"])
    # write all chapters --> chapter breakdown test
    write_to_json("chapters.json", chapter_boundaries)

    aligned_chapters = align_chapters_with_whisper(
        chapter_boundaries["chapters"], transcription["segments"])
    write_to_json("aling_chapters.json", aligned_chapters)

    return aligned_chapters if aligned_chapters else []


def chapter_breakdown(transcription_txt):
    """Break down the transcription text using gemma2:2b model"""
    print(ollama_url)
    ollama_rq = {
        "model": ollama_model,
        "prompt": json.dumps(create_ollama_prompt(transcription_txt)),
        "stream": False,
        "format": "json"
    }
    generate_url = ollama_url + "/api/generate"
    try:
        response = requests.post(generate_url, json=ollama_rq, headers=headers)
        response.raise_for_status()
        result = response.json()

        # Parse the JSON string
        data = json.loads(result["response"])
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def create_ollama_prompt(transcription_text):
    prompt = f"""You are a video transcription analyzer. Your task is to break down the following video transcription into structured chapters.

    Go thorugh the transcription and IDENTIFY KEY TOPICS or CHANGES in SUBJECT MATTER. Split the transcription into chapters based on these topics.
    
    Rules for processing:
    1. Keep the exact wording from the transcription in the "content" field
    2. Do not paraphrase or modify the original text
    3. Split chapters based on clear topic changes or natural pauses
    4. Each chapter must contain direct quotes from the transcription

    Required JSON structure:
    {{
    "chapters": [
        {{
        "chapterNumber": [number],
        "title": [brief descriptive title, max 8 words],
        "content": [exact text from transcription for this section],
        "startTime": [timestamp if available, otherwise omit]
        }}
    ],
    "metadata": {{
        "totalChapters": [number],
        "mainTopics": [array of key topics covered]
    }}
    }}

    Transcription:
    {transcription_text}"""

    return prompt


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(datetime.timedelta(seconds=int(seconds)))

def get_words(text: str) -> Set[str]:
    """Convert text to a set of cleaned words."""
    # Clean text by removing punctuation and converting to lowercase
    cleaned = ''.join(c.lower() for c in text if c.isalnum() or c.isspace())
    return set(cleaned.split())


def find_chapter_segments(chapter_content: str,
                          segments: List[Dict[str, Any]],
                          required_coverage: float = 0.85) -> tuple:
    """
    Find the minimal set of consecutive segments that cover the chapter content.

    Args:
        chapter_content: The text content of the chapter
        segments: List of transcript segments
        required_coverage: Minimum percentage of chapter words that must be found

    Returns:
        tuple: (start_index, end_index) or (None, None) if no match found
    """
    chapter_words = get_words(chapter_content)
    total_chapter_words = len(chapter_words)

    best_start = None
    best_end = None
    min_segments_needed = float('inf')

    # Try each segment as a potential starting point
    for start_idx in range(len(segments)):
        current_words = set()

        # Accumulate segments until we have sufficient coverage
        for end_idx in range(start_idx, len(segments)):
            segment_text = segments[end_idx]['text']
            current_words.update(get_words(segment_text))

            # Calculate word coverage
            common_words = chapter_words.intersection(current_words)
            coverage = len(common_words) / total_chapter_words

            # Check if we have sufficient coverage
            if coverage >= required_coverage:
                segments_needed = end_idx - start_idx + 1
                # Update if we found a shorter sequence that meets our coverage
                if segments_needed < min_segments_needed:
                    min_segments_needed = segments_needed
                    best_start = start_idx
                    best_end = end_idx
                break

            # If we've accumulated too many extra words, break this attempt
            if len(current_words) > total_chapter_words * 2:
                break

    return best_start, best_end


def align_chapters_with_whisper(chapters: List[Dict[str, Any]],
                                segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Align chapters with Whisper segments using word-based matching.
    """
    aligned_chapters = []
    current_segment_idx = 0

    for chapter in chapters:
        # Find matching segments for this chapter
        start_idx, end_idx = find_chapter_segments(
            chapter["content"],
            segments[current_segment_idx:]
        )

        if start_idx is not None and end_idx is not None:
            # Adjust indices based on current_segment_idx
            start_idx += current_segment_idx
            end_idx += current_segment_idx

            # Create aligned chapter
            aligned_chapter = {
                "chapterNumber": chapter["chapterNumber"],
                "title": chapter["title"],
                "content": chapter["content"],
                "start": segments[start_idx]["start"],
                "end": segments[end_idx]["end"],
                "segments": list(range(start_idx, end_idx + 1))
            }

            # Update current_segment_idx for next iteration
            current_segment_idx = end_idx + 1
        else:
            # If no matching segments found
            aligned_chapter = {
                "chapterNumber": chapter["chapterNumber"],
                "title": chapter["title"],
                "content": chapter["content"],
                "start": None,
                "end": None,
                "segments": []
            }

        aligned_chapters.append(aligned_chapter)

    return aligned_chapters


def write_to_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
