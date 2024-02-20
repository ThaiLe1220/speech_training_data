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


if __name__ == "__main__":
    FILE_NAME = "obama3_transcribed"
    input_file_path = f"./transcribe/{FILE_NAME}.txt"
    output_file_path = f"./transcribe/{FILE_NAME}_processed.txt"

    processed_text_lines = process_text_to_audio_chunks(input_file_path)

    # Write the processed text to a new file
    with open(output_file_path, "w") as output_file:
        for line in processed_text_lines:
            output_file.write(line + "\n")

    print(f"Processed text has been saved to {output_file_path}")
