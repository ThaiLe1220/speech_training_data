""" Filename: utils.py - Directory: ./ """

# Import necessary libraries
from pytube import YouTube  # To handle downloading from YouTube
import ffmpeg  # For converting video to audio
import speech_recognition as sr  # For converting speech to text
import time  # To calculate process duration
import os  # For file path operations and file deletion
from pydub import AudioSegment  # For audio manipulation
import soundfile as sf  # For handling WAV file sample rates


def download_youtube_audio_as_wav(url, output_dir, filename):
    """
    Downloads and converts a YouTube video's audio stream to a WAV file
    and removes the intermediary MP4 file.
    """
    # Create a YouTube object with the URL
    yt = YouTube(url)

    # Get the audio stream with the highest bitrate
    audio_stream = yt.streams.get_audio_only()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the path to the downloaded MP4 file
    mp4_path = os.path.join(output_dir, filename + ".mp4")

    # Download the audio stream as MP4
    audio_stream.download(output_path=output_dir, filename=filename + ".mp4")

    # Define the path for the output WAV file
    wav_path = os.path.join(output_dir, filename + ".wav")

    # Convert MP4 to WAV using ffmpeg
    ffmpeg.input(mp4_path).output(wav_path).run(overwrite_output=True)

    # Delete the MP4 file after conversion to free up space
    os.remove(mp4_path)


def convert_audio(input_path, output_path, target_sample_rate=22050):
    """
    Converts an audio file to a specific sample rate and format (WAV),
    handling mono conversion if necessary.
    """
    # Load the original WAV file
    original_audio = AudioSegment.from_file(input_path, format="wav")

    # Convert to mono if stereo and set the target sample rate
    mono_audio = original_audio.set_channels(1)
    converted_audio = mono_audio.set_frame_rate(target_sample_rate)

    # Export the converted file
    converted_audio.export(output_path, format="wav")

    # Verify and fix the sample rate using soundfile if necessary
    data, sample_rate = sf.read(output_path)
    if sample_rate != target_sample_rate:
        # Correct the sample rate and rewrite if incorrect
        sf.write(output_path, data, target_sample_rate)
        print(f"Fixed the sample rate to {target_sample_rate} Hz.")
    else:
        print(f"Audio successfully converted to {target_sample_rate} Hz.")


def transcribe_audio(audio_file_path, output_text_file):
    """
    Transcribes audio from a file to text using Google's speech recognition API.
    """
    # Initialize recognizer
    r = sr.Recognizer()

    # Start time for process estimation
    start_time = time.time()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        print("Processing audio file...")
        audio_data = r.record(source)  # Load audio to memory for processing

    try:
        # Recognize speech using Google's speech recognition
        print("Transcribing audio...")
        text = r.recognize_google(audio_data, language="vi-VN")
        with open(output_text_file, "w", encoding="utf-8") as file:
            file.write(text)
        print("Transcription complete and saved to", output_text_file)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    # End time for process duration estimation
    end_time = time.time()
    print(f"Process completed in {end_time - start_time:.2f} seconds.")
