# Media Analyzer Project

## Overview
The Media Analyzer project is a FastAPI application designed to analyze video files, generating transcripts and chapters using various AI models. This project includes a frontend interface for users to upload videos and view the generated chapters.

## Project Structure
- **api/**: Contains the backend FastAPI application.
- **test-fe/**: Contains the frontend code for the user interface.
- **scripts/**: Contains utility scripts for audio extraction and text matching.

## API Documentation
The API is built using FastAPI and provides endpoints for video analysis. The main endpoint is:

- **POST /api/media-analyzer/vid-to-text**: Upload a video file to get the transcript and chapters.

### Running the API
To run the API, follow these steps:
1. Clone the repository.
2. Move into **api/** using `cd api/` 
3. Follow the instructions in api [API README](api/README.md)

The API will be available at `http://localhost:8000`.

## Frontend (test-fe)
The frontend is built using HTML, CSS, and JavaScript. It allows users to upload video files and view the generated chapters. The main components include:

- **index.html**: The main HTML file that sets up the video player and upload interface.
- **styles.css**: The CSS file for styling the frontend components.
- **script.js**: The JavaScript file that handles video uploads, fetches data from the backend, and updates the UI with chapter information.

### Key Features
- Video upload functionality.
- Dynamic chapter generation and display.
- Interactive video timeline with chapter markers.

## Scripts
The scripts directory contains utility scripts for processing audio and matching text segments. Key scripts include:

- **aud_extractor.py**: A script to extract audio from video files using MoviePy.
- **text_matcher.py**: A script that includes functions to calculate text similarity and align chapters with their corresponding segments.



## Conclusion
This project provides a comprehensive solution for video analysis, allowing users to easily upload videos and receive structured chapter information. For more details on the API, refer to the API documentation in the [`api/README.md`](api/README.md) file.
