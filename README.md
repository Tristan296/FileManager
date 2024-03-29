# FileManager
![image](https://github.com/Tristan296/FileManager/assets/109927879/63bf6873-0b07-4478-b40a-dd737f4a1a7c)



## Files:
- ```GUI.py``` is the Graphical Interface version.
- ```FileManager.py``` is the Command Line version.

## Setup: 

### GUI File Manager:
Before use, please install PyQt5 please run the following command in the python terminal.
- Windows: ```pip install pyqt5 zipfile bz2 subprocess``` 
- MacOs: ```sudo pip3 install pyqt5 zipfile bz2 subprocess```
  
## Functions you can perform on files/folders: 
1. Search through computer or specific paths
2. Directly open files
3. Move files into folders
4. Rename files
5. Select multiple files
6. Copy files
7. Delete Files
8. Create new folders
9. Compress both files and folders to ZIP or BZ2 formats
10. Batch rename multiple files with naming pattern
11. Get File details (path, size, last modified data and creation date)
    
## Troubleshooting (MacOS):
### PyQt5 didn't install properly:
```
Traceback (most recent call last):
  File "/Users/tristan/Desktop/Programming/FileManager/FileManager/GUI.py", line 5, in <module>
    from PyQt5.QtWidgets import *
```
#### Install brew and use the following command:
```
brew install pyqt5
```
