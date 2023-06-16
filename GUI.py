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
    QLabel,
    QGridLayout
)
import subprocess
import platform
import shutil
from pathlib import Path
import bz2
import zipfile

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


def move_file(filePath, folder_path):
    shutil.move(filePath, folder_path)


def open_file(findPath):
    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", findPath))
    elif platform.system() == "Windows":  # Windows
        os.startfile(findPath)
    else:  # linux variants
        subprocess.call(("xdg-open", findPath))


class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)

        self.searcher = FileSearcher(
            "/"
        )  # Create a FileSearcher object with root path '/'
        layout = self.layout()
        self.verticalLayout = QVBoxLayout(self) 

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)
        self.verticalLayout.addWidget(browse_button)

        compress_button_bz2 = QPushButton("Compress to bz2")
        compress_button_bz2.clicked.connect(self.compress_files_bz2)
        self.verticalLayout.addWidget(compress_button_bz2)

        compress_button_zip = QPushButton("Compress to zip")
        compress_button_zip.clicked.connect(self.compress_files_zip)
        self.input_field = QLineEdit()
        self.verticalLayout.addWidget(compress_button_zip)
    
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        self.verticalLayout.addWidget(exit_button)
        
        layout.addLayout(self.verticalLayout, layout.rowCount(), 0, 1, layout.columnCount())
        self.setLayout(layout)
        
    def resizeEvent(self, event):
        # Override the resizeEvent method to set the window size
        self.resize(600, 700)  # Set the desired width and height


    def browse(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.searcher = FileSearcher(folder_path)

    def open(self):
        for file_path in self.selectedFiles():
            open_file(file_path)

    def compress_files_zip(self): 
        for file_path in self.selectedFiles():
            if file_path:
                archive = f"{Path(file_path).stem}.zip"
                with zipfile.ZipFile(archive, "w") as zf:
                    zf.write(file_path)
                    shutil.move(archive, f'{Path.cwd()}/misc/zip/')

    def compress_files_bz2(self):
        for file_path in self.selectedFiles():
            if file_path:
                compressed_filepath = file_path + ".bz2"
                with open(file_path, "rb") as file_in:
                    with bz2.BZ2File(compressed_filepath, "wb") as file_out:
                        shutil.copyfileobj(file_in, file_out)
                        shutil.move(compressed_filepath, f'{Path.cwd()}/misc/bz2/')
                print("File compressed successfully.")
            else: 
                print("File failed to compress.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = FileDialog()
    dialog.resize(500, 300)
    if dialog.exec_() == QFileDialog.Accepted:
        dialog.selected_files = dialog.selectedFiles()
        print(dialog.selected_files)
    sys.exit(app.exec_())