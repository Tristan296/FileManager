import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QMimeData, QUrl
import subprocess
import platform
import shutil
from pathlib import Path
import bz2
import zipfile
from zipfile import ZipFile

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
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(findPath)
    else:  # linux variants
        subprocess.call(('xdg-open', findPath))

class FileDialog(QFileDialog):
    selected_files = []

    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.searcher = FileSearcher("/")  # Create a FileSearcher object with root path '/'
        self.setup_UI()

    def setup_UI(self):  # initialize setup UI
        self.setWindowTitle("FileManager")

        self.resize(900, 500)  # setup window center and resizing
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        set_layout = QHBoxLayout()  # set of layouts

        group_boxF = QGroupBox("File Manager")
        main_layout = self.layout()
        group_boxF.setLayout(main_layout)

        group_boxG = QGroupBox("Features")
        group_boxG.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        button_layout = QVBoxLayout()
        
        compress_bz2_button = QPushButton("Compress to BZ2")
        compress_bz2_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        compress_bz2_button.clicked.connect(self.compress_files_bz2)
        button_layout.addWidget(compress_bz2_button)
        
        compress_zip_button = QPushButton("Compress to ZIP")
        compress_zip_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        compress_zip_button.clicked.connect(self.compress_files_zip)
        button_layout.addWidget(compress_zip_button)        
        
        unzip_button = QPushButton("unzip")
        unzip_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        unzip_button.clicked.connect(self.unzip_files)
        button_layout.addWidget(unzip_button)

        duplicate_file_button = QPushButton("Duplicate")
        duplicate_file_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        duplicate_file_button.clicked.connect(self.duplicate_file)
        button_layout.addWidget(duplicate_file_button)
    
        exit_button = QPushButton("Exit")
        exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        group_boxG.setLayout(button_layout)

        global status_label
        status_label = QTextBrowser()
        status_label.setAcceptRichText(True)

        sub1_layout = QHBoxLayout()
        sub1_layout.addWidget(group_boxF)

        sub3_layout = QHBoxLayout()
        sub3_layout.addWidget(group_boxG)

        set_layout.addLayout(sub1_layout)

        set_layout.addLayout(sub3_layout)

        self.setLayout(set_layout)

    def path(self, dir):
        FileDialog.selected_files = dir


    def compress_files_zip(self): 
        for file_path in self.selectedFiles():
            if file_path:
                archive = f"{Path(file_path).stem}.zip"
                with zipfile.ZipFile(archive, "w") as zf:
                    zf.write(file_path)
                    shutil.move(archive, f'{Path.cwd()}/misc/archived/ZIP/')
    
    def unzip_files(self): 
        for file_path in self.selectedFiles():
            if file_path:
                file_extension = Path(file_path).suffix

                if file_extension == '.zip':
                    with zipfile.ZipFile(file_path, 'r') as archive:
                        archive.extractall(f'{Path.cwd()}/misc/unarchived/ZIP/')
                    print("ZIP file unzipped successfully.")
                elif file_extension == '.bz2':
                    output_file = f'{Path.cwd()}/misc/unarchived/BZ2/{Path(file_path).stem}'
                    with open(output_file, 'wb') as output:
                        with bz2.BZ2File(file_path, 'rb') as archive:
                            shutil.copyfileobj(archive, output)
                    print("BZ2 file unzipped successfully.")
                else:
                    print("Unsupported file format.")
            else:
                print("No file selected.")

    def compress_files_bz2(self):
        for file_path in self.selectedFiles():
            if file_path:
                compressed_filepath = file_path + ".bz2"
                with open(file_path, "rb") as file_in:
                    with bz2.BZ2File(compressed_filepath, "wb") as file_out:
                        shutil.copyfileobj(file_in, file_out)
                        shutil.move(compressed_filepath, f'{Path.cwd()}/misc/archived/BZ2/')
                print("File compressed successfully.")
            else: 
                print("File failed to compress.")
                
    def duplicate_file(self):
        for file_path in self.selectedFiles():
            if file_path:
                file_name = os.path.basename(file_path)
                file_directory = os.path.dirname(file_path)
                duplicate_path = os.path.join(file_directory, f"Copy of {file_name}")

                try:
                    shutil.copy2(file_path, duplicate_path)
                    print(f"File '{file_name}' duplicated successfully.")
                except FileNotFoundError:
                    print(f"The file '{file_name}' does not exist.")
                except PermissionError:
                    print(f"Permission denied. Unable to duplicate the file '{file_name}'.")
                except Exception as e:
                    print(f"An error occurred while duplicating the file '{file_name}': {str(e)}")
            else:
                print("No file selected.")

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()

    while (dialog.exec_() == QFileDialog.Accepted): 
        print(dialog.selectedFiles()) 
        dialog.selected_files = dialog.selectedFiles()
        dialog.path(dialog.selectedFiles())
        dialog.show()

    sys.exit(app.exec_())
