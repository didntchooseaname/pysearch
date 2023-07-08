import os
import re
from collections import defaultdict

if __name__ == "__main__":
    print(r"""
__________    _____  ________                      
\______   \  /     \ \______ \  __ ________  ______
 |       _/ /  \ /  \ |    |  \|  |  \____ \/  ___/
 |    |   \/    Y    \|    `   \  |  /  |_> >___ \ 
 |____|_  /\____|__  /_______  /____/|   __/____  >
        \/         \/        \/      |__|       \/ 

 ▶️  Find and remove duplicates string in all text files of a directory. Takes a long time on larger files.    
      """)

def find_duplicate_strings(directory):
    duplicates = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                duplicates = find_duplicate_strings_in_file(filepath, duplicates)

    return duplicates

def find_duplicate_strings_in_file(file, duplicates):
    strings = defaultdict(list)
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        for line_number, line in enumerate(f, start=1):
            cleaned_line = re.sub(r'[^-\w/.]+', '', line.strip())
            strings[cleaned_line].append((file, line_number))

    for string, occurrences in strings.items():
        if len(occurrences) > 1:
            duplicates[string] += occurrences

    return duplicates

def remove_duplicates(duplicates):
    total_duplicates = len(duplicates)
    processed_duplicates = 0

    for string, occurrences in duplicates.items():
        for file, line_number in occurrences:
            lines = []
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            lines = [line for i, line in enumerate(lines, start=1) if not (i == line_number and re.sub(r'[^-\w/.]+', '', line.strip()) == string)]

            with open(file, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            processed_duplicates += 1
            percentage = (processed_duplicates / total_duplicates) * 100
            print(f"Removing duplicates... {percentage:.2f}% complete")

# Ask the directory to search in
root_directory = input("Directory to search in ('.' for current directory): ")

# Check if the input directory is accessible
while not os.path.isdir(root_directory):
    print("The specified directory does not exist. Please try again.")
    root_directory = input("Directory to search in ('.' for current directory): ")

# Find duplicate strings within files
duplicate_strings = find_duplicate_strings(root_directory)

# Display the found duplicates
if duplicate_strings:
    print("Duplicate strings found:")
    for string, occurrences in duplicate_strings.items():
        if len(occurrences) > 1:
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