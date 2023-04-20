<<<<<<< Updated upstream
import PySimpleGUI as sg # for GUI interface
import subprocess, os, platform
import pathlib
from re import search
import sys
from traceback import TracebackException
from types import TracebackType

def findfile(name, path): 
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)
        
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
# Event Loop to process "events" and get the "values" of the inputs

while True:
    event, values = window.read()
    filename = values[0]
    filetype = values[1]
    filepath = values[2]
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    # if the 'OK' Button is pressed.
    if event == 'Computer': 
        findPath = findfile(filename + "." + filetype, "/")
        if findPath == None: 
            sg.popup("Your file couldn't be found, Please try again.")
        else: 
            sg.popup_ok(f"Your file was found at {findPath}")

    elif event == 'OK': 
        filepath = findfile(filename + "." + filetype, "/Users/trist/" + filepath)
        print('Found the file with the following path:', filepath)
        print("---" * 30)
        
    elif event == 'Open': 
        try: 
            open_file(findPath)
        
        except NameError as e:
            sg.popup_error(f"Error:{e}",'Please re-input file name and search before opening.')
        
window.close()
=======
import sys
from PyQt6.QtCore import QDir, QFile, QIODevice, QTextStream
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
)

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("File Manager")
        self._createWidgets()
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createWidgets(self):
        # Tree View
        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabel("Name")
        self.setCentralWidget(self.tree_view)

    def _createMenu(self):
        menu = self.menuBar().addMenu("&File")

        # Open action
        open_action = menu.addAction("&Open", self._open_file)
        open_action.setShortcut("Ctrl+O")

        # Save action
        save_action = menu.addAction("&Save", self._save_file)
        save_action.setShortcut("Ctrl+S")

        # Save As action
        save_as_action = menu.addAction("Save &As", self._save_file_as)
        save_as_action.setShortcut("Ctrl+Shift+S")

        menu.addSeparator()

        # Exit action
        exit_action = menu.addAction("&Exit", self.close)
        exit_action.setShortcut("Ctrl+Q")

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

    def _open_file(self):
    	file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*);;Text Files (*.txt)")
		if file_path:
        	# Clear the tree view
        	self.tree_view.clear()
            root_item = QTreeWidgetItem()
            root_item.setText(0, file_path)
            self.tree_view.addTopLevelItem(root_item)
            self._populate_tree_view(file_path, root_item)

    def _populate_tree_view(self, directory, parent_item):
        dir = QDir(directory)
        for entry in dir.entryList(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot):
            item = QTreeWidgetItem()
            item.setText(0, entry)
            parent_item.addChild(item)

            entry_path = dir.filePath(entry)
            if dir.exists(entry_path) and dir.isDir(entry_path):
                self._populate_tree_view(entry_path, item)

	def _save_file(self):
		current_item = self.tree_view.currentItem()
		if current_item is not None:
			file_path, _ = QFileDialog.getSaveFileName(self, "Save File", current_item.text(0), "Text Files (*.txt)")
			if file_path:
				# Save the file
				with QFile(file_path) as file:
					if file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
						stream = QTextStream(file)
						text = current_item.text(0)
						stream << text
						file.close()

    def _save_file_as(self):
		current_item = self.tree_view.currentItem()
		if current_item is not None:
			file_path, _ = QFileDialog.getSaveFileName(self, "Save File", current_item.text(0), "Text Files (*.txt)")
			if file_path:
				# Save the file
				with QFile(file_path) as file:
					if file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
						stream = QTextStream(file)
						text = current_item.text(0)
						stream << text
						file.close()

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
>>>>>>> Stashed changes
