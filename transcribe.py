from faster_whisper import WhisperModel
import os
import re  # Import the regular expressions module

# Attempt to use a GPU if available, otherwise fall back to CPU
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
model_size = "large-v3"
model = WhisperModel(model_size, device=device)


def transcribe(audio_file_path):
    try:
        segments, info = model.transcribe(
            audio=audio_file_path,
            beam_size=6,  # Increased beam size for better accuracy
            temperature=0,  # Kept at 0 for deterministic outputs
            word_timestamps=True,
            condition_on_previous_text=True,  # Enable to consider context
            no_speech_threshold=0.1,  # Adjust based on testing with your audio files
        )

        segment_list = []
        for segment in segments:
            segment_dict = {
                "start": "%.2f" % segment.start,
                "end": "%.2f" % segment.end,
                "text": segment.text,
            }

            segment_list.append(segment_dict)

        # Join the text segments into a single sentence
        joined_text = " ".join([segment["text"] for segment in segment_list])

        return joined_text

    except Exception as e:
        return str(e)


def transcribe_folder(input_folder, output_file, audio_name):
    transcriptions = []  # List to hold filename and transcription result tuples

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav") and filename.startswith(audio_name):
            audio_file_path = os.path.join(input_folder, filename)
            transcription_result = transcribe(audio_file_path)

            # Add cleaned filename and transcription result to the list
            transcriptions.append((audio_file_path, transcription_result))
            print(filename + " Done!")

    # Sort the list by filenames in ascending order
    transcriptions.sort(key=lambda x: x[0])

    # Write the sorted results to the output file
    with open(output_file, "w") as out_file:
        for filename, transcription in transcriptions:
            out_file.write(f"{filename}{transcription}\n")


if __name__ == "__main__":

    print("Running in process...")
    AUDIO = "obama3"

    transcribe_folder("./split/", f"./transcribe/{AUDIO}_transcribed.txt", AUDIO)
