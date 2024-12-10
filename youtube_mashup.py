import os
import yt_dlp
from pydub import AudioSegment
import argparse
import threading

def download_video(result, download_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',  # Reduced quality for faster download
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Downloading: {result['title']} from {result['webpage_url']}")
            ydl.download([result['webpage_url']])
        except Exception as e:
            print(f"Error downloading {result['title']}: {e}")

def download_audio(keyword, num_videos, download_dir):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{num_videos}:{keyword}", download=False)['entries']

        threads = []
        for result in search_results:
            thread = threading.Thread(target=download_video, args=(result, download_dir))
            threads.append(thread)
            thread.start()

            # To limit the number of concurrent downloads
            if len(threads) % 5 == 0:
                for t in threads:
                    t.join()
                threads.clear()

        # Join remaining threads
        for t in threads:
            t.join()

def process_audios(trim_duration, output_file):
    audio_paths = [file for file in os.listdir('.') if file.endswith('.mp3')]
    print(f"Detected mp3 files: {audio_paths}")

    if not audio_paths:
        print("No audio files were detected after download.")
        return

    combined = AudioSegment.empty()
    for path in audio_paths:
        try:
            print(f"Processing file: {path}")
            audio = AudioSegment.from_file(path)
            if len(audio) > trim_duration * 1000:
                trimmed_audio = audio[:trim_duration * 1000]
                combined += trimmed_audio
                print(f"Trimmed and added: {path}")
            else:
                print(f"Audio file {path} is shorter than {trim_duration} seconds, skipped trimming.")
        except Exception as e:
            print(f"Error processing {path}: {e}")

    if combined:
        combined.export(output_file, format="mp3")
        print(f"Combined audio saved as {output_file}")
    else:
        print("No audio files were combined.")

def main():
    parser = argparse.ArgumentParser(description="Download and combine YouTube audio clips.")
    parser.add_argument('keyword', type=str, help='Search keyword for YouTube videos.')
    parser.add_argument('num_videos', type=int, help='Number of videos to download.')
    parser.add_argument('trim_duration', type=int, help='Duration in seconds to trim from each audio file.')
    parser.add_argument('output_file', type=str, help='Output file name for the combined audio.')

    args = parser.parse_args()

    print(f"Downloading {args.num_videos} audio files for '{args.keyword}'...")
    download_audio(args.keyword, args.num_videos, './')

    print(f"Processing audios to trim and combine into {args.output_file}...")
    process_audios(args.trim_duration, args.output_file)

if __name__ == "__main__":
    main()
