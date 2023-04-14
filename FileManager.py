import os
import shutil
import sys
import pathlib
import subprocess

# Define the global variable for filepath
filepath = ""
filetype = ""

def moveFile(foundfile=None):
    if not foundfile:
        return

    while True:
        createFolder = input("Create a new Folder (Y/N) : ").upper()
        print("---" * 30)
        if "YES" in createFolder or createFolder == "Y":
            while True:
                folder_name = input("Enter folder name to create: ")
                folder_dest_path = os.path.join("/Users/tristan/", folder_name)
                if not os.path.exists(folder_dest_path):
                    os.makedirs(folder_dest_path)
                    print("Folder created successfully!")
                    print("---" * 30)
                    break
                else:
                    print("Folder already exists. Please choose a different name.")
                    print("---" * 30)

        elif "NO" in createFolder or createFolder == "N":
            ParentName = input("What is the parent of this folder : ")
            print("---" * 30)
            FindFolder = input("Enter folder name to move file into : ")
            print("---" * 30)
            folder_dest_path = os.path.join("/Users/tristan/", ParentName, FindFolder)
            print("destination path", folder_dest_path)
            verify = input("Are you sure you want to do this? (Y/N) : ").upper()
            print("---" * 30)

            if verify == "YES" or verify == "Y" or verify == "y":
                try:
                    shutil.move(foundfile, folder_dest_path)
                    print("File moved successfully!")
                    break

                except shutil.Error as e:
                    print("Error while moving file:", e)
                    break

                except Exception as e:
                    print("Error:", e)
                    break

        else:
            print("Please ensure that you answer either yes or no.")
            print("---" * 30)

def openFile(found_file=None):
    if not found_file:
        found_file = input("Enter the file name to search and open: ")

    file_found = False
    for dirpath, dirnames, filenames in os.walk('/Users/tristan/'):  # Update the base directory to search for files
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
manageFile = input("Enter 'move' to move a file, 'open' to search and open a file, or 'search' to search the entire computer: ")

while True:
    if "move" in manageFile:
        filepath = input("Enter the file path: ")
        filetype = input("Enter the file type: ")
        filename = input("Enter the file name: ")
        moveFile()
    elif "open" in manageFile:
        filepath = input("Enter the file path: ")
        filetype = input("Enter the file type: ")
        filename = input("Enter the file name: ")
        openFile(found_file)
    elif "search" in manageFile:
        found_file = searchComputer()
        while found_file:
            manageFile = input("What do you want to do with the file? (move/open/search)")
            if "move" in manageFile:
                moveFile(found_file)
            elif "open" in manageFile: 
                openFile(found_file)
            elif "search" in manageFile:
                found_file = searchComputer()
            else:
                print("Invalid input. Please enter 'move', 'open', or 'search'.")
    else:
        print("Invalid input. Please try again .")

