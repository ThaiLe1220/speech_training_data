""" Filename: main.py - Directory: ./ """

from pytube import YouTube
import ffmpeg
import os
import speech_recognition as sr


def process_youtube_audio(url, output_dir):
    """
    Downloads audio from a YouTube video, converts it to WAV, and transcribes it.

    Args:
    url (str): The URL of the YouTube video.
    output_dir (str): Directory where the WAV and transcription files will be saved.

    Returns:
    tuple: Path to the saved WAV file and path to the saved transcription text file.
    """
    # Initialize paths and filenames
    filename = "downloaded_audio"
    os.makedirs(output_dir, exist_ok=True)
    mp4_path = os.path.join(output_dir, filename + ".mp4")
    wav_path = os.path.join(output_dir, filename + ".wav")
    transcript_path = os.path.join(output_dir, filename + "_transcription.txt")

    # Download the audio from YouTube
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(output_path=output_dir, filename=filename + ".mp4")

    # Convert the downloaded MP4 to WAV
    ffmpeg.input(mp4_path).output(wav_path).run(overwrite_output=True)
    os.remove(mp4_path)  # Clean up the MP4 file

    # Transcribe the WAV file
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)  # Load audio to memory
        try:
            text = recognizer.recognize_google(audio_data, language="vi-VN")
            with open(transcript_path, "w") as file:
                file.write(text)
        except (sr.UnknownValueError, sr.RequestError) as e:
            print(f"Error during transcription: {e}")
            text = ""

    print("Processing complete. WAV and transcription files saved.")
    return (wav_path, transcript_path)


# Example usage:
url = "https://www.youtube.com/watch?v=FWINvusp1U8"
output_dir = "./output"
wav_file, transcript_file = process_youtube_audio(url, output_dir)
print(f"WAV file saved at: {wav_file}")
print(f"Transcription saved at: {transcript_file}")
