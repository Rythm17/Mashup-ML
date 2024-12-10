# YouTube Mashup
This audio compilation script creates audio mashups by downloading, trimming, and compiling audio from YouTube videos based on a keyword search.

## Features
Keyword Search: Fetches YouTube videos related to a user-defined keyword.

Audio Download: Extracts audio from videos.

Trimming: Trims a user-specified duration from the start of each audio.

Compilation: Combines trimmed audio clips into a single MP3 file.

Custom Output: Allows naming the final output file.

## Requirements
Install dependencies:
```bash
   pip install pytube pydub moviepy
```

## Usage
1. Run the script:
```bash
   python youtube_mashup.py
```
2. Provide inputs:
   
   a. Keyword (e.g., "Lo-fi music").

   b. Number of videos (e.g., 5).

   c. Trim duration (e.g., 30 seconds).

   d. Output file name (e.g., "lofi_mashup").

## Outputs
The final mashup is saved as an MP3 file (e.g., lofi_mashup.mp3).


