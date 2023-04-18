import os
import shutil
import subprocess

def moveFile(filepath):
    if filepath:
        print("File found at: " + filepath)
        print("---" * 30)
        choice = input("What do you want to do with the file? (move/open/search) ").lower()
        if choice == "move":
            parent_folder = input("What is the parent of this folder: ")
            folder_name = input("Enter folder name to move file into: ")
            destination_path = os.path.join(os.path.expanduser("~"), parent_folder, folder_name)
            print("Destination path: " + destination_path)
            confirm = input("Are you sure you want to do this? (Y/N): ").lower()
            if confirm == "y":
                try:
                    os.makedirs(destination_path, exist_ok=True)
                    shutil.move(filepath, os.path.join(destination_path, os.path.basename(filepath)))
                    print("File moved successfully!")
                except Exception as e:
                    print("Error: " + str(e))
            else:
                print("File not moved.")
        elif choice == "open":
            openFile(filepath)
        elif choice == "search":
            pass
        else:
            print("Invalid choice. Please choose from 'move', 'open', or 'search'.")
    else:
        print("File not found.")

def openFile(found_file=None):
    if not found_file:
        found_file = input("Enter the file name to search and open: ")

    file_found = False
    for dirpath, dirnames, filenames in os.walk(os.path.expanduser("~")):  # Update the base directory to search for files
        for file in filenames:
            if found_file in file:
                found_file = os.path.join(dirpath, file)
                file_found = True
                break
        if file_found:
            break

    if file_found:
        print("File found at:", found_file)
        subprocess.run(['open', found_file])  # Open the file with default macOS application
    else:
        print("File not found.")

        
def searchComputer():
    filename = input("Enter the file name to search: ")
    filetype = input("Enter the file type: ")
    found_file = None
    for dirpath, dirnames, filenames in os.walk('/'):  # Update the base directory to search for files
        for file in filenames:
            if filename in file and file.endswith("." + filetype):
                found_file = os.path.join(dirpath, file)
                break
        if found_file:
            break

    if found_file:
        print("File found at:", found_file)
        return found_file
    
    else:
        print("File not found.")
        return None

# Update the code to set the filepath variable before calling moveFile or openFile

def main():
    global filepath
    while True:
        print("1. Move File")
        print("2. Open File")
        print("3. Search Computer")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")
        print("---" * 30)
        
        if choice == "1":
                filepath = searchComputer()
                moveFile(filepath)
                filepath = ""

        elif choice == "2":
            filepath = searchComputer()
            openFile(filepath)
            filepath = ""

        elif choice == "3":
            filepath = searchComputer()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please choose from 1, 2, 3, or 4.")
            print("---" * 30)

if __name__ == "main":
    main()

