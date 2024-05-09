from pytube import YouTube
import ffmpeg
import os

# URL of the YouTube video
url = "https://www.youtube.com/shorts/3924Sw03-mU"

# Create a YouTube object with the URL
yt = YouTube(url)

# Get the audio stream with the highest bitrate
audio_stream = yt.streams.get_audio_only()

# Define the output directory and filename without extension
output_dir = "./output"
filename = "downloaded_audio"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Download the audio stream as mp4
audio_stream.download(output_path=output_dir, filename=filename + ".mp4")

# Define the path to the downloaded MP4 file
input_path = os.path.join(output_dir, filename + ".mp4")

# Define the path for the output WAV file
output_path = os.path.join(output_dir, filename + ".wav")

# Convert mp4 to wav using the paths
(ffmpeg.input(input_path).output(output_path).run(overwrite_output=True))

print("Download and conversion complete!")
