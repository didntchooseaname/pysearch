import os

print(r"""
__________         _________                           .__     
\______   \___.__./   _____/ ____ _____ _______   ____ |  |__  
 |     ___<   |  |\_____  \_/ __ \\__  \\_  __ \_/ ___\|  |  \ 
 |    |    \___  |/        \  ___/ / __ \|  | \/\  \___|   Y  \
 |____|    / ____/_______  /\___  >____  /__|    \___  >___|  /
           \/            \/     \/     \/            \/     \/ 

 ▶️  Quickly find any string in all txt files of a directory.     
      """)

def search_words_in_directory(directory, word):
    count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                file_count = search_words_in_file(filepath, word)
                count += file_count
                if file_count > 0:
                    print(f"'{word}' was found {file_count} times in '{filename}'")
    if count == 0:
        print("Entry not found.")

def search_words_in_file(file, word):
    count = 0
    with open(file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            if word.lower() in line.lower():
                count += 1

    return count

# Root directory from which the search should begin
root_directory = './'

# Continue to request input until "exit" is entered or Ctrl+C is pressed
while True:
    word_to_search = input("Search a string (or 'exit' to quit): ")
    if word_to_search.lower() == 'exit' or word_to_search.lower() == 'quit':
        break
    search_words_in_directory(root_directory, word_to_search)
