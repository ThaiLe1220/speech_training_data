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


import re
import os


def clean_text(text):
    # Remove unwanted unicode characters (adjust pattern as needed)
    clean_text = re.sub(r"[^\w\s.,'!?]+", "", text)

    # Normalize multiple spaces into single spaces
    clean_text = re.sub(r"\s+", " ", clean_text)

    return clean_text.strip()  # Remove extra leading/trailing whitespace


def process_text_to_audio_chunks(file_path):
    processed_lines = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)  # Split on space, maximum of 1 split
            if len(parts) == 2:
                audio_path, text = parts
                # Extract base name and number from audio path
                file_name = os.path.basename(
                    audio_path
                )  # Use for cross-platform compatibility
                base_name, _, suffix = file_name.partition("_chunk_")
                chunk_number = suffix.split(".")[0]

                # Clean the text content
                text = clean_text(text)

                new_line = f"audio/{base_name}_chunk_{chunk_number}.wav|{text}"
                processed_lines.append(new_line)

    # Sorting logic remains as before
    processed_lines.sort(
        key=lambda x: (
            x.split("|")[0].rsplit("_", 2)[0],
            int(x.split("_")[-1].split(".")[0]),
        )
    )

    return processed_lines


# if __name__ == "__main__":
#     FILE_NAME = "obama3_transcribed"
#     input_file_path = f"./transcribe/{FILE_NAME}.txt"
#     output_file_path = f"./transcribe/{FILE_NAME}_processed.txt"

#     processed_text_lines = process_text_to_audio_chunks(input_file_path)

#     # Write the processed text to a new file
#     with open(output_file_path, "w") as output_file:
#         for line in processed_text_lines:
#             output_file.write(line + "\n")

#     print(f"Processed text has been saved to {output_file_path}")

from pydub import AudioSegment
import os


def is_silence_chunk(dB_levels, min_len=500, max_len=5000, avg_dB_thresh=-20):
    """Check if the dB level list represents a silence chunk."""
    duration = len(dB_levels) * 1  # Assuming 1 ms per dB level for simplicity
    if not min_len <= duration <= max_len:
        return False
    avg_dB = sum(dB_levels) / len(dB_levels)
    return avg_dB < avg_dB_thresh


def segment_chunks(speech_chunks, min_length=4000, max_length=15000):
    """Segment or merge speech chunks to ensure they are within 5s to 15s."""
    segmented_chunks = []
    for start, end in speech_chunks:
        chunk_length = end - start
        if chunk_length < min_length:
            if (
                segmented_chunks
                and (segmented_chunks[-1][1] - segmented_chunks[-1][0] + chunk_length)
                <= max_length
            ):
                # Merge with the previous chunk if the total length is within the limit
                prev_start, prev_end = segmented_chunks.pop()
                segmented_chunks.append((prev_start, end))
            else:
                # If it cannot be merged, adjust to minimum length or leave as is
                # This could involve either leaving short chunks or extending them slightly
                # Decision may depend on application-specific requirements
                segmented_chunks.append((start, end))  # Adjust this logic as needed
        elif chunk_length > max_length:
            # Segment long chunks into smaller ones
            for segment_start in range(start, end, max_length):
                segment_end = min(segment_start + max_length, end)
                segmented_chunks.append((segment_start, segment_end))
        else:
            # Chunk is within the desired range
            segmented_chunks.append((start, end))
    return segmented_chunks


def extract_speech_chunks(
    file_path,
    output_folder,
    output_file_name,
    min_silence_len=500,
    silence_thresh=-25,
    min_length=4000,
    max_length=15000,
):
    audio = AudioSegment.from_file(file_path)
    silence_start = None
    dB_levels = []
    speech_chunks = []
    last_speech_end = 0

    for i in range(0, len(audio), 1):  # Analyze every 1 ms
        segment = audio[i : i + 1]
        dB = segment.dBFS

        if dB < silence_thresh:  # Potential silence
            if silence_start is None:  # Mark the start of a silence segment
                silence_start = i
            dB_levels.append(dB)
        else:
            if silence_start is not None:
                # Evaluate the potential silence chunk
                if is_silence_chunk(
                    dB_levels, min_len=min_silence_len, avg_dB_thresh=silence_thresh
                ):
                    # If it's silence, save the previous speech chunk
                    if last_speech_end < silence_start:
                        speech_chunks.append((last_speech_end, silence_start))
                    last_speech_end = i
                # Reset for next potential silence segment
                silence_start = None
                dB_levels = []

    # Check for a final speech chunk
    if last_speech_end < len(audio):
        speech_chunks.append((last_speech_end, len(audio)))

    # Segment or merge speech chunks to ensure they fit within the desired length range
    speech_chunks = segment_chunks(
        speech_chunks, min_length=min_length, max_length=max_length
    )

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Export the speech chunks
    for index, (start, end) in enumerate(speech_chunks, start=1):
        if index == 1:
            # For the first chunk, extend the end by 200 but don't change the start
            chunk = audio[start + 6000 : end + 300]
        elif index == len(speech_chunks):
            # For the last chunk, extend the start by 200 but don't extend the end
            chunk = audio[start - 300 : end]
        else:
            # For all other chunks, extend both start and end by 200
            chunk = audio[start - 300 : end + 300]

        chunk_name = os.path.join(
            output_folder, f"{output_file_name}_chunk_{index}.wav"
        )
        chunk.export(chunk_name, format="wav")
        print(f"Exported {chunk_name}")
