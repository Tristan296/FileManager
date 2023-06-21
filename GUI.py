import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
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

        group_boxF = QGroupBox("File Browser")
        main_layout = self.layout()
        group_boxF.setLayout(main_layout)

        group_boxG = QGroupBox("Features")
        group_boxG.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        button_layout = QVBoxLayout()
        
        compressBz2 = QPushButton("Compress to BZ2")
        compressBz2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        compressBz2.clicked.connect(self.compress_files_bz2)
        button_layout.addWidget(compressBz2)
        
        compressZip = QPushButton("Compress to ZIP")
        compressZip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        compressZip.clicked.connect(self.compress_files_zip)
        button_layout.addWidget(compressZip)        

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


    def create_new_file(self):  # create file
        try:
            new_file_name, ok = QInputDialog.getText(self, 'New File', 'Enter name for new file:')  
            while ok and not new_file_name.strip():  # 파일 이름이 없는 경우를 처리
                QMessageBox.warning(self, "Invalid File Name", "File name cannot be empty. Please enter again.")
                new_file_name, ok = QInputDialog.getText(self, 'New File', 'Enter name for new file:')
            if ok:
                file_path = FileDialog.selected_files[0]
                file_location, file_name = os.path.split(file_path)

                new_file_path = os.path.join(file_location, new_file_name)

                uniq = 1
                while os.path.exists(new_file_path): 
                    new_file_path = os.path.join(file_location, new_file_name + "(" + str(uniq) + ")")
                    uniq += 1
                if uniq > 1:
                    new_file_name += "(%d)" % (uniq - 1) 
                open(new_file_path, 'w').close() 
                QMessageBox.information(self, "Create New File", f"New file created: {new_file_name} in {new_file_path}")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    
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
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()

    while (dialog.exec_() == QFileDialog.Accepted): 
        print(dialog.selectedFiles()) 
        dialog.selected_files = dialog.selectedFiles()
        dialog.path(dialog.selectedFiles())
        dialog.show()

    sys.exit(app.exec_())
