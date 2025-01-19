# Media Analyzer API

This project is a FastAPI application that analyzes video files and generates transcripts and chapters using various AI models.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add the following variables:

   ```plaintext
   OLLAMA_API=<your_ollama_api_url>
   OLLAMA_MODEL=<your_ollama_model>
   GEMINI_API_KEY=<your_gemini_api_key>
   GEMINI_MODEL=<your_gemini_model>
   ```

   Replace `<your_ollama_api_url>`, `<your_ollama_model>`, `<your_gemini_api_key>`, and `<your_gemini_model>` with your actual API details.

## Running the API

To start the FastAPI server, run the following command:

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- **POST /api/media-analyzer/vid-to-text**: Upload a video file to get the transcript and chapters.

## Testing the API

You can test the API using tools like Postman or curl. Here's an example using curl:

```bash
curl -X POST "http://localhost:8000/api/media-analyzer/vid-to-text" -F "file=@<path_to_your_video_file>"
```

Replace `<path_to_your_video_file>` with the path to the video file you want to analyze.
