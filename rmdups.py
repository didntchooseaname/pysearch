import os
import re
from collections import defaultdict
from tqdm import tqdm

def find_duplicate_strings(directory):
    duplicates = defaultdict(list)
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                file_count += 1

    progress_bar = tqdm(total=file_count, desc="Searching duplicates")

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                duplicates = find_duplicate_strings_in_file(filepath, duplicates)
                progress_bar.update(1)

    progress_bar.close()
    return duplicates

def find_duplicate_strings_in_file(file, duplicates):
    strings = defaultdict(list)
    with open(file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            stripped_line = line.strip()
            cleaned_line = re.sub(r'[^-\w/.]+', '', stripped_line)
            strings[cleaned_line].append((file, line_number))
    for string, occurrences in strings.items():
        if len(occurrences) > 1:
            duplicates[string] += occurrences
    return duplicates

def remove_duplicates(duplicates):
    progress_bar = tqdm(total=len(duplicates), desc="Removing duplicates")
    for string, occurrences in duplicates.items():
        for file, line_number in occurrences:
            lines = []
            with open(file, 'r') as f:
                lines = f.readlines()

            lines = [line for i, line in enumerate(lines, start=1) if not (i == line_number and re.sub(r'[^-\w/.]+', '', line.strip()) == string)]

            with open(file, 'w') as f:
                f.writelines(lines)

            progress_bar.update(1)
    progress_bar.close()

# Directory containing the text files to analyze
root_directory = './'

# Find duplicate strings within files
duplicate_strings = find_duplicate_strings(root_directory)

# Display the found duplicates
if duplicate_strings:
    print("Duplicate strings found:")
    for string, occurrences in duplicate_strings.items():
        if occurrences:
            print(f"String: '{string}' ({len(occurrences)} duplicates)")
            for file, line_number in occurrences:
                print(f"- File: {file}, Line: {line_number}")

    # Prompt the user to remove duplicates
    choice = input("Do you want to remove the duplicates? (yes/no): ")
    if choice.lower() == 'yes':
        remove_duplicates(duplicate_strings)
        print("Duplicates removed.")
    else:
        print("Duplicates not removed.")
else:
    print("No duplicate strings found.")
