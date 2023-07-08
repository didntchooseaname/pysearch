import os

print(r"""
__________         _________                           .__     
\______   \___.__./   _____/ ____ _____ _______   ____ |  |__  
 |     ___<   |  |\_____  \_/ __ \\__  \\_  __ \_/ ___\|  |  \ 
 |    |    \___  |/        \  ___/ / __ \|  | \/\  \___|   Y  \
 |____|    / ____/_______  /\___  >____  /__|    \___  >___|  /
           \/            \/     \/     \/            \/     \/ 

 ▶️  Quickly find any string in all text files of a directory.     
      """)

###################################################
#                 CONFIGURATION                   #
###################################################

# Root directory from which the search should begin
root_directory = './'

###################################################
#              END OF CONFIGURATION               #
###################################################

def search_words_in_directory(directory, word):
    count = 0
    txt_files_found = False  # Variable to track if text files are found
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                txt_files_found = True  # Set to True if a text file is found
                filepath = os.path.join(root, filename)
                file_count = search_words_in_file(filepath, word)
                count += file_count
                if file_count > 0:
                    print(f"✅ '{word}' was found {file_count} times in '{filename}'")
    
    if not txt_files_found:  # Check if no text files are found
        print("❌ No text files found.")  # Display the corresponding message
    
    if count == 0 and txt_files_found:  # Check if no occurrences are found in the text files
        file_count = count_text_files(directory)
        print(f"❌ Entry '{word}' not found in {file_count} text files")

def search_words_in_file(file, word):
    count = 0
    with open(file, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            if word.lower() in line.lower():
                count += 1

    return count

def count_text_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                count += 1
    return count

# Continue to request input until "exit" is entered or Ctrl+C is pressed
while True:
    word_to_search = input("🔎 Enter a search string (or 'exit' to quit): ")
    if word_to_search.lower() == 'exit' or word_to_search.lower() == 'quit':
        break
    search_words_in_directory(root_directory, word_to_search)
