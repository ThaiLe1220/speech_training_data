from datasets import load_dataset
import nltk
from nltk.tokenize import word_tokenize
import random
import re

# Ensure you have the NLTK tokenizer resources
nltk.download("punkt")


def save_vietnamese_text(dataset, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for split in dataset.keys():
            for example in dataset[split]:
                file.write(example["translation"]["vi"] + "\n")


def count_unique_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    tokens = word_tokenize(text)
    unique_tokens = set(tokens)
    return len(unique_tokens), unique_tokens


def clean_line(line):
    # Remove special characters
    special_chars = '()"-_'
    for char in special_chars:
        line = line.replace(char, "")

    # Fix spacing around commas
    line = line.replace(" ,", ",")
    line = line.replace("  ", " ")
    line = line.replace(";", ",")
    line = line.replace("…", ".")
    line = line.replace("...", ".")

    # Trim periods from the beginning or the end of the line and excess spaces
    line = line.strip(",. ;")

    # Ensure the line does not exceed 200 characters
    return line[:200]


def generate_random_text(input_path1, input_path2, output_path, max_chars=1000000):
    # Read all lines from the first file
    with open(input_path1, "r", encoding="utf-8") as file:
        lines1 = file.readlines()

    # Read all lines from the second file
    with open(input_path2, "r", encoding="utf-8") as file:
        lines2 = set(file.readlines())

    # Define a regular expression pattern for Vietnamese text and specific punctuation
    pattern = re.compile(
        r'^[a-zA-Zàáảãạăắằẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ\s,\.?!;%"…()_-]+$'
    )

    # Filter lines based on character length, pattern, and non-appearance in input_path2
    short_lines = [
        line.strip()
        for line in lines1
        if 18 <= len(line.strip()) <= 45 and pattern.match(line) and line not in lines2
    ]
    medium_lines = [
        line.strip()
        for line in lines1
        if 45 < len(line.strip()) <= 145 and pattern.match(line) and line not in lines2
    ]
    long_lines = [
        line.strip()
        for line in lines1
        if 145 < len(line.strip()) <= 180 and pattern.match(line) and line not in lines2
    ]

    # Adjust the proportions
    random.shuffle(medium_lines)
    random.shuffle(short_lines)
    random.shuffle(long_lines)

    # Determine the total number of lines desired, assuming a maximum number available
    total_available_lines = len(medium_lines) + len(short_lines) + len(long_lines)
    target_proportion = 0.7

    # Calculate numbers for target and other lines to achieve the desired proportion
    num_target = int(total_available_lines * target_proportion)
    num_other = total_available_lines - num_target  # Remaining lines

    # Ensure we don't request more target lines than available
    num_target = min(num_target, len(medium_lines))
    num_other = min(num_other, len(short_lines) + len(long_lines))

    # Assemble the final list of lines
    total_lines = medium_lines[:num_target] + random.sample(
        short_lines + long_lines, num_other
    )

    # Shuffle the combined list to randomize the selection process
    random.shuffle(total_lines)

    # Initialize output text and process the shuffled lines
    output_text = ""
    for line in total_lines:
        clean_and_trimmed_line = clean_line(line)
        if clean_and_trimmed_line:
            if len(output_text) + len(clean_and_trimmed_line) > max_chars:
                break
            output_text += clean_and_trimmed_line + "\n"

    # Write the output text to a new file
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(output_text)


def main():
    # Specify the output file path
    output_file_path = "all_vietnamese_texts.txt"

    # Save the Vietnamese texts
    # save_vietnamese_text(load_dataset("Eugenememe/mix-en-vi-4m"), output_file_path)

    # Count unique words and print them
    # unique_word_count, unique_words = count_unique_words(output_file_path)
    # print(f"Total unique words: {unique_word_count}")  # 800k unique words

    # Call the function to generate the file
    generate_random_text(
        "src/all_vietnamese_texts.txt",
        "src/vi_universal_2m.txt",
        "src/vi_universal_1m_plus.txt",
    )

    unique_word_count, unique_words = count_unique_words("src/vi_universal_1m_plus.txt")
    print(f"Total unique words: {unique_word_count}")  # 14k unique words


if __name__ == "__main__":
    main()
