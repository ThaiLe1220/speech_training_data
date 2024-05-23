import os
import re
import random
from collections import Counter

# List of Vietnamese characters
vietnamese_characters = (
    "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơ"
    "ƠƯĂÂĐÊÔƠƯ1234567890ăâêôơư"
    "ĂÂÁẢÃẠẤẦẨẪẬẮẰẲẴẶ"
    "đĐÊỀÉẸẺẼẾỀỂỄỆ"
    "ÍÌỈĨỊ"
    "ÔỐỒỔỖỘƠỚỜỞỠỢ"
    "ÚÙỦŨỤƯỨỪỬỮỰ"
    "ÝỲỶỸỴýỳỷỹỵ"
    "áàạảã"
    "âấầẩẫậ"
    "ăắằẳẵặ"
    "đ"
    "éèẹẻẽ"
    "êếềểễệ"
    "íìịỉĩ"
    "óòọỏõ"
    "ôốồổỗộ"
    "ơớờởỡợ"
    "úùụủũ"
    "ưứừửữự"
    "ýỳỵỷỹ"
)


def is_vietnamese_char(char):
    return char in vietnamese_characters


def is_vietnamese_line(line):
    count = sum(1 for char in line if is_vietnamese_char(char))
    return count / len(line) > 0.25


def merge_text_files(src_dir, output_file):
    with open(output_file, "w") as outfile:
        for filename in os.listdir(src_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(src_dir, filename)
                with open(file_path, "r") as infile:
                    for line in infile:
                        cleaned_line = line.strip()
                        if 13 <= len(cleaned_line) <= 200:
                            if not re.search(r'[-;>>*"”“…)\[\]\'’+_]', cleaned_line):
                                if is_vietnamese_line(cleaned_line):
                                    outfile.write(cleaned_line + "\n")


def convert_to_lowercase(input_file, output_file):
    seen_lines = set()
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            lower_line = line.lower().strip()
            if lower_line and lower_line not in seen_lines:
                seen_lines.add(lower_line)
                outfile.write(lower_line + "\n")


def select_random_lines(input_file, output_file, num_lines):
    with open(input_file, "r") as infile:
        lines = infile.readlines()
    random.shuffle(lines)
    selected_lines = lines[:num_lines]
    with open(output_file, "w") as outfile:
        outfile.writelines(selected_lines)
    return selected_lines


def count_unique_words(lines):
    word_counter = Counter()
    for line in lines:
        words = re.findall(r"\b\w+\b", line)
        word_counter.update(words)
    return len(word_counter)


src_dir = "src/collection"
merged_file = "src/collection_merge.txt"
lowercase_file = "src/collection_merge_lc.txt"
selected_file = "src_collection_unique.txt"

# # Step 1: Merge the text files
# merge_text_files(src_dir, merged_file)
# print(f"Merged files into {merged_file}")

# # Step 2: Convert the merged file to lowercase
# convert_to_lowercase(merged_file, lowercase_file)
# print(f"Converted all characters to lowercase in {lowercase_file}")

# Step 3: Randomly select 50,000 lines from the lowercase file
selected_lines = select_random_lines(lowercase_file, selected_file, 25000)
print(f"Selected 25,000 lines and saved to {selected_file}")

# Step 4: Count the total number of unique words in the selected lines
unique_word_count = count_unique_words(selected_lines)
print(f"Total number of unique words: {unique_word_count}")
