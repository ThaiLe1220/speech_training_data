import speech_recognition as sr
import time
import os


def transcribe_audio(audio_file_path, output_text_file):
    # Initialize recognizer
    r = sr.Recognizer()

    # Start time for estimation
    start_time = time.time()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        print("Processing audio file...")
        audio_data = r.record(source)  # Load audio to memory

    try:
        # Recognize speech using Google's speech recognition
        print("Transcribing audio...")
        text = r.recognize_google(audio_data, language="vi-VN")
        with open(output_text_file, "w") as file:
            file.write(text)
        print("Transcription complete and saved to", output_text_file)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )

    # End time for estimation
    end_time = time.time()
    print(f"Process completed in {end_time - start_time:.2f} seconds.")


# Define paths
audio_file_path = "output/downloaded_audio.wav"
output_text_file = "output/audio_transcribe.txt"

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Call the function
transcribe_audio(audio_file_path, output_text_file)
