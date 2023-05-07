import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox,
)
import subprocess
import platform
import shutil
import pathlib

class FileSearcher:
    def __init__(self, root_path):
        self.root_path = root_path

    def search_file(self, name, filetype):
        for dirpath, dirname, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename == f"{name}":
                    return os.path.join(dirpath, filename)
        return None

    def list_files(self):
        return os.listdir(self.root_path)

    def get_user_name(self):
        return getpass.getuser()


def move_file(filePath, folder_path):
    shutil.move(filePath, folder_path)

def open_file(findPath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(findPath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', findPath))


class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.searcher = FileSearcher("/")  # Create a FileSearcher object with root path '/'
        self.selected_files = []

        layout = self.layout()

        # Add widgets for file searching and manipulation
        self.filename_input = QLineEdit()
        layout.addWidget(self.filename_input)

        self.filetype_combo = QLineEdit()
        layout.addWidget(self.filetype_combo)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)
        layout.addWidget(browse_button)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        move_button = QPushButton("Move File")
        move_button.clicked.connect(self.move)
        layout.addWidget(move_button)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open)
        layout.addWidget(open_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)
        

    def browse(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.searcher = FileSearcher(folder_path)

    def search(self):
        filename = self.filename_input.text()
        filetype = self.filetype_combo.text()
        file_list = self.searcher.list_files()
        filtered_files = [
            f for f in file_list if f.endswith(filetype) and filename in f
        ]
        if filtered_files:
            self.selectFile(os.path.join(self.searcher.root_path, filtered_files[0]))
        else:
            QMessageBox.warning(self, "Warning", "No files found in the selected directory.")

    def move(self):
        if self.selectedFiles():
            folder_path = QFileDialog.getExistingDirectory()
            if folder_path:
                for file_path in self.selectedFiles():
                    move_file(file_path, folder_path)
                    QMessageBox.information(
                        self,
                        "Information",
                        f"Your File has been moved succesfully from {file_path} to {folder_path}!",
                    )
                self.selected_files.clear()
        else:
            QMessageBox.warning(
                self, 
                "Warning"
                "No files selected.",
            )
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()
    if dialog.exec_() == QFileDialog.Accepted:
        print(dialog.selectedFiles())
    sys.exit(app.exec_())
