import PySimpleGUI as sg
import subprocess, os, platform
import pathlib

class FileSearcher:
    def __init__(self, root_path):
        self.root_path = root_path

    def search_file(self, name, filetype):
        for dirpath, dirname, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename == f"{name}.{filetype}":
                    return os.path.join(dirpath, filename)
        return None

def open_file(findPath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(findPath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', findPath))

sg.theme('DarkGrey7')

file_types = ['exe', 'txt', 'jpg', 'png', 'docx', 'pdf', 'mp4']

layout = [  [sg.Text('Input File Name') , sg.InputText()],
            [sg.Combo(file_types, size=(20, 6))],
            [sg.Text('Search Options:')],
            [sg.Button('Computer')], # Browsing Lets you select a directory to search in.
            [sg.Text('Enter Path'), sg.InputText()],
            [sg.Text('Select Function:')],
            [sg.Button('Open'), sg.Button('Move'), sg.Button('Duplicate'), sg.Button('Delete')],
            [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('FileManager', layout)

# Create a FileSearcher object with root path '/'
searcher = FileSearcher("/")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    filename = values[0]
    filetype = values[1]
    filepath = values[2]
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    # if the 'Computer' Button is pressed.
    if event == 'Computer': 
        findPath = searcher.search_file(filename, filetype)
        if findPath == None: 
            sg.popup("Your file couldn't be found, Please try again.")
        else: 
            sg.popup_ok(f"Your file was found at {findPath}")

    elif event == 'OK': 
        # Search for the file in the specified directory
        findPath = searcher.search_file(filename, filetype)
        if findPath is None:
            sg.popup_error("File not found")
        else:
            print(f"Found the file with the following path: {findPath}")
            print("---" * 30)
        
    elif event == 'Open': 
        try: 
            open_file(findPath)
        
        except NameError as e:
            sg.popup_error(f"Error:{e}",'Please re-input file name and search before opening.')
        
window.close()
