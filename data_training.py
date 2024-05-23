import random


# Function to read data from a file
def read_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines


# Function to write data to a file
def write_data(filename, lines):
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)


# Read data from files
data1 = read_data("src/filtered_vi_universal_3.txt")
# data2 = read_data("src/filtered_vi_universal_1m.txt")

# Combine and shuffle the data
# combined_data = data1 + data2
combined_data = data1
random.shuffle(combined_data)

# Split data into training and validation sets (85% train, 15% val)
split_index = int(0.85 * len(combined_data))
train_data = combined_data[:split_index]
val_data = combined_data[split_index:]

# Write the split data to files
write_data("output/train.txt", train_data)
write_data("output/val.txt", val_data)

print("Data has been split and saved successfully.")
