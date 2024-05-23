import os


def extract_number(file_name):
    """
    Extract the number from the filename assuming the format 'audio_{number}_...'.
    """
    base_name = os.path.basename(file_name)
    number_part = base_name.split("_")[1]
    return int(number_part)


def find_wav_files(directory_path):
    """
    Walk through the directory, collect all .wav files, and sort them by the numerical value after 'audio_'.
    """
    wav_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".wav"):
                wav_files.append(os.path.join(root, file))
    wav_files.sort(key=extract_number)
    return wav_files


def find_max_number(wav_files):
    """
    Find the maximum number among the .wav filenames.
    """
    max_number = max(extract_number(file) for file in wav_files)
    return max_number


def find_missing_numbers(wav_files, max_number):
    """
    Identify missing numbers in the sequence up to max_number.
    """
    existing_numbers = {extract_number(file) for file in wav_files}
    all_numbers = set(range(1, max_number + 1))
    missing_numbers = sorted(all_numbers - existing_numbers)
    return missing_numbers


def write_missing_numbers(missing_numbers, file_path):
    """
    Write missing numbers to a file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for number in missing_numbers:
            f.write(f"{number}\n")
    print(f"Missing numbers written to {file_path}")


def load_transcriptions(file_path):
    """
    Load all transcriptions from a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        transcriptions = file.readlines()
    print("Total transcriptions loaded:", len(transcriptions))  # Debug print
    return transcriptions


def filter_transcriptions(transcriptions, wav_files):
    """
    Filter the transcriptions to only include those for which the corresponding .wav file exists.
    Assumes transcriptions are sorted and aligned with the sorted .wav file list.
    Adds full path before each transcription.
    """
    filtered_transcriptions = []
    wav_file_numbers = sorted({extract_number(file) for file in wav_files})
    wav_files_dict = {
        extract_number(file): file for file in wav_files
    }  # Dictionary to map number to file path

    for number in wav_file_numbers:
        try:
            # Get the full path from the wav_files_dict
            full_path = wav_files_dict[number]
            # Assume the transcriptions are in a 1-indexed file format matching the .wav files
            transcription_line = f"{full_path}|{transcriptions[number-1].strip()}\n"
            filtered_transcriptions.append(transcription_line)
        except IndexError:
            print(f"Index error with number: {number}, possible missing transcription.")
            continue

    return filtered_transcriptions


def write_transcriptions(filtered_transcriptions, file_path):
    """
    Write filtered transcriptions to a new file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(filtered_transcriptions)

    print(
        f"Filtered transcriptions written to {file_path}, count: {len(filtered_transcriptions)}"
    )


def main():
    """
    Main function to run the program.
    """

    directory_path = "wavs/universal3"
    transcription_file_path = "src/vi_universal_3.txt"
    output_file_path = "src/filtered_vi_universal_3.txt"

    wav_files = find_wav_files(directory_path)
    max_number = find_max_number(wav_files)
    missing_numbers = find_missing_numbers(wav_files, max_number)
    write_missing_numbers(missing_numbers, "src/universal_missing_3.txt")

    all_transcriptions = load_transcriptions(transcription_file_path)
    filtered_transcriptions = filter_transcriptions(all_transcriptions, wav_files)
    write_transcriptions(filtered_transcriptions, output_file_path)


if __name__ == "__main__":
    main()
