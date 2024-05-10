from datasets import load_dataset
import nltk
from nltk.tokenize import word_tokenize
import random

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


def generate_random_text(input_path, output_path, max_chars=1000):
    # Read all lines from the file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Remove any newline characters from the lines
    lines = [line.strip() for line in lines if line.strip()]

    # Shuffle the lines to randomize the selection process
    random.shuffle(lines)

    # Concatenate lines until the maximum number of characters is reached
    output_text = ""
    for line in lines:
        if len(output_text) + len(line) > max_chars:
            break
        output_text += line + "\n"  # Add the line and a newline character

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
    generate_random_text("all_vietnamese_texts.txt", "random_vietnamese_texts_1000.txt")


if __name__ == "__main__":
    main()
