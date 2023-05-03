import PySimpleGUI as sg
import subprocess, os, platform
import shutil
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

    def list_files(self):
        return os.listdir(self.root_path)
    
def move_file(filePath, folder_path):
    shutil.move(filePath, folder_path)

def open_file(findPath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(findPath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', findPath))

sg.theme('')

file_types = ['exe', 'txt', 'jpg', 'png', 'docx', 'pdf', 'mp4']

column_to_be_centered = [
    [sg.Button('Move File'), sg.Button('Open'), sg.Button('Exit')]
]

layout = [  [sg.Text('File Name:') , sg.InputText(key='-FILENAME-')],
            [sg.Text('File Type:'), sg.Combo(file_types, size=(20, 6), key='-FILETYPE-'), sg.Button('Browse'), sg.Button('Search')],
            [sg.Listbox([], size=(80, 20), key='-LISTBOX-')],
            [sg.VPush()],
            [sg.VPush(), sg.Column(column_to_be_centered, element_justification='c')],
]
# Create the Window
window = sg.Window('FileManager', layout)

# Create a FileSearcher object with root path '/'
searcher = FileSearcher("/")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    filename = values['-FILENAME-']
    filetype = values['-FILETYPE-']
    findPath = searcher.search_file(filename, filetype)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    # if the 'Computer' Button is pressed.
    
    elif event == 'Search': 
        file_list = searcher.list_files()
        if file_list:
            window['-LISTBOX-'].update(file_list)
        else:
            sg.popup("No files found in the selected directory.")
    elif event == 'Open': 
        if findPath is None:
            sg.popup_error('Please select a file to open.')
        else:
            try: 
                open_file(findPath)
            
            except IndexError:
                sg.popup_error('Please select a file to open.')
    elif event == 'Browse':
        folder_path = sg.popup_get_folder('Select a folder to search in')
        if folder_path:
            searcher = FileSearcher(folder_path)

    elif event == 'Search': 
        file_list = searcher.list_files()
        if file_list:
            window['-LISTBOX-'].update(file_list)
        else:
            sg.popup("No files found in the selected directory.")
    
    elif event == 'Move File':
        folder_path = sg.popup_get_folder('Select a folder to move file into')
        if folder_path:
            move = move_file(findPath, folder_path)
            sg.popup_ok(f'Your File has been moved succesfully from {findPath} to {folder_path}!')
            
    elif event == 'Exit':
        window.close()
        
window.close()
