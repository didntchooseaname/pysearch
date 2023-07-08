import os
import multiprocessing

def search_words_in_file(file, word):
    count = 0
    with open(file, 'r', errors='ignore') as f:
        for line in f:
            if word.lower() in line.lower():
                count += 1
    return count

def search_words_in_directory(args):
    directory, word = args
    count = 0
    results = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                file_count = search_words_in_file(filepath, word)
                count += file_count
                if file_count > 0:
                    results.append((filename, file_count))
    
    return count, results

def count_text_files(directory):
    count = 0
    for root, _, files in os.walk(directory):
        count += sum(filename.endswith('.txt') for filename in files)
    return count

if __name__ == "__main__":
    print(r"""
__________         _________                           .__     
\______   \___.__./   _____/ ____ _____ _______   ____ |  |__  
 |     ___<   |  |\_____  \_/ __ \\__  \\_  __ \_/ ___\|  |  \ 
 |    |    \___  |/        \  ___/ / __ \|  | \/\  \___|   Y  \
 |____|    / ____/_______  /\___  >____  /__|    \___  >___|  /
           \/            \/     \/     \/            \/     \/ 

 ▶️  Quickly find any string in all text files of a directory.     
      """)

    while True:
        # Ask the directory to search in
        root_directory = input("➡️  Directory to search in ('.' for current directory): ")

        # Check if the input directory is accessible
        if not os.path.isdir(root_directory):
            print("❌ The specified directory does not exist. Please try again.")
        else:
            break

    # Continue to request input until "exit" is entered or Ctrl+C is pressed
    while True:
        word_to_search = input("\n🔎 Enter a string to search (or 'exit' to quit): ")
        if word_to_search.lower() in ('exit', 'quit'):
            break
        
        # Create a list of directory-word pairs for multiprocessing
        search_args = [(root_directory, word_to_search)]

        num_processes = multiprocessing.cpu_count()  # Number of processes to use
        with multiprocessing.Pool(processes=num_processes) as pool:
            total_files = count_text_files(root_directory)
            completed_files = 0

            results = []
            # Use the map function to process the search in parallel
            for count, result in pool.imap_unordered(search_words_in_directory, search_args):
                results.extend(result)
                completed_files += count

            # Display the results
            if results:
                print("\n🔍 Search Results:")
                for filename, file_count in results:
                    print(f"✅ '{word_to_search}' was found {file_count} times in '{filename}'")
            else:
                print(f"\n❌ Entry '{word_to_search}' not found in any text files.")