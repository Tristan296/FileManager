# This Universal File Manager has many functions. 
# It can search for specific files throughout the entire computer, or within a certain folder.
# It can also move files to different locations, duplicate, delete export or open files.

# TODO: Still need to make it so a file can be searched for within a path for faster searching.

import os
import sys
import subprocess
import pathlib
from re import search
import shutil
from traceback import TracebackException
from types import TracebackType
from alive_progress import alive_bar

def findfile(name, path): 
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

filename = input("Input File Name: ")
print("---" * 30)
filetype = input("Input File Type (Don't include '.') :  ").lower()
print("---" * 30)

while True:
    searchType = input("Would you like to search entire computer(1) or just in a path(2)? : ")
    print("---" * 30)

    if "computer" in searchType or searchType == '1': 
        filepath = findfile(filename + "." + filetype, "/")  
        print("The path of the file is:", filepath)
        print("---" * 30)
        break

    elif "path" in searchType or searchType == '2':
        findPath = input("Enter name of path to search in : ")
        filepath = findfile(filename + "." + filetype, "/Users/trist/" + findPath)
        print('Found the file with the following path:', filepath)
        print("---" * 30)
        break

    else: 
        print("Please ensure you chose one of the options.")
        print("---" * 30)


manageFile = input("""What would you like to do with this file? : 
     1. Move to different directory. 
     5. Open
""")

def moveFile():
    def compute(): # Progress Bar
        for i in range(1):
            shutil.move(filepath, folder_dest_path)
            yield

    while True: 
        global filepath
        createFolder = input("Create a new Folder (Y/N) : ").upper()
        print("---" * 30)
        if "YES" in createFolder or createFolder == "Y": 
            pathlib.Path().resolve()

        elif "NO" in createFolder or createFolder == "N":
            ParentName = input("What is the parent of this folder : ")
            print("---" * 30)
            FindFolder = input("Enter folder name to move file into : ")
            print("---" * 30)
            folder_dest_path = "/users/trist/" + ParentName + "/" + FindFolder # ! This requires proper fixing
            print("destination path", folder_dest_path)
            verify = input("Are you sure you want to do this? (Y/N) : ").upper()
            print("---" * 30)

            if verify == "YES" or verify == "Y":
                try:
                    with alive_bar(1) as bar:
                        for i in compute():
                            bar()
                            
                except Exception:
                    print('It seems this File already exists. Please change the file name to something else : ')
                    new_name = input("Input New file name: ")
                    new_file_name_path = "/users/trist/" + ParentName + "/" + new_name + "." + filetype
                    os.rename(filepath, new_file_name_path)
                    print("Your File name was changed to", new_name, "and was moved Sucessfully!")
                    break
                break

        else: 
            print("Please ensure that you answer either yes or no.")
            print("---" * 30)
            
def openFile():
    sys.path.append(filepath)
    subprocess.Popen('explorer "C:\\temp"')

if "move" in manageFile:    
    moveFile()
if "open" in manageFile:
    openFile()