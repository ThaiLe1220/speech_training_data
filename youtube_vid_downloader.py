import os
from yt_dlp import YoutubeDL
import ffmpeg


def get_video_title(url):
    """
    Extracts the video title from the given YouTube URL.

    Args:
    url (str): The URL of the YouTube video.

    Returns:
    str: The title of the video.
    """
    ydl_opts = {"quiet": True, "format": "best", "extract_flat": True}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict["title"]


def sanitize_filename(filename):
    """
    Sanitizes a string to be used as a valid filename.

    Args:
    filename (str): The original filename.

    Returns:
    str: The sanitized filename.
    """
    return "".join(c if c.isalnum() else "_" for c in filename)


def download_youtube_video_audio(url, output_dir):
    """
    Downloads a video and audio from YouTube, saves them as MP4 and WAV files,
    and combines them into a final MP4 file with audio.

    Args:
    url (str): The URL of the YouTube video.
    output_dir (str): Directory where the files will be saved.

    Returns:
    tuple: Paths to the saved WAV audio file and final MP4 video with audio.
    """
    # Get the video title to use as the filenames
    video_title = get_video_title(url)
    sanitized_title = sanitize_filename(video_title)

    # Initialize paths and filenames
    temp_video_mp4_path = os.path.join(output_dir, sanitized_title + "_temp.mp4")
    audio_wav_path = os.path.join(output_dir, sanitized_title + ".wav")
    final_mp4_path = os.path.join(output_dir, sanitized_title + ".mp4")

    os.makedirs(output_dir, exist_ok=True)

    # Options for yt-dlp to download video without audio
    ydl_video_opts = {
        "format": "bestvideo",
        "outtmpl": temp_video_mp4_path,
    }

    # Options for yt-dlp to download audio only
    ydl_audio_opts = {
        "format": "bestaudio",
        "outtmpl": os.path.join(output_dir, sanitized_title + ".%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    # Download the video (without audio)
    with YoutubeDL(ydl_video_opts) as ydl:
        ydl.download([url])

    # Download the audio (as WAV)
    with YoutubeDL(ydl_audio_opts) as ydl:
        ydl.download([url])

    # Combine video and audio into final MP4 file
    input_video = ffmpeg.input(temp_video_mp4_path)
    input_audio = ffmpeg.input(audio_wav_path)
    ffmpeg.output(
        input_video, input_audio, final_mp4_path, vcodec="copy", acodec="aac"
    ).run(overwrite_output=True)

    # Remove the temporary video file
    os.remove(temp_video_mp4_path)

    print(f"Download and processing complete for {url}")
    return audio_wav_path, final_mp4_path


def process_video_list(input_file, output_dir):
    """
    Processes a list of YouTube URLs from a file, downloading and combining video and audio for each.

    Args:
    input_file (str): Path to the input file containing YouTube URLs.
    output_dir (str): Directory where the files will be saved.
    """
    with open(input_file, "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            download_youtube_video_audio(url, output_dir)


# Example usage:
input_file = "input/video.txt"
output_dir = "./output"
process_video_list(input_file, output_dir)
