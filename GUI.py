import os
import sys
import subprocess
import pathlib
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

root = Tk()
root.title("File Manager")

style = ttk.Style()
style.configure("TButton",
                font=('Helvetica', 14),
                padding=10)
style.configure("TLabel",
                font=('Helvetica', 14),
                padding=10)
style.configure("TFrame",
                padding=20)

def browse_file():
    global filepath
    filepath = filedialog.askopenfilename()
    file_label.config(text="Selected File: " + filepath)

def browse_folder():
    global folderpath
    folderpath = filedialog.askdirectory()
    folder_label.config(text="Selected Folder: " + folderpath)

def move_file():
    global filepath, folderpath
    if filepath and folderpath:
        file_name = os.path.basename(filepath)
        destination = os.path.join(folderpath, file_name)
        if os.path.exists(destination):
            messagebox.showerror("Error", "File already exists in the destination folder. Please choose a different folder.")
        else:
            try:
                shutil.move(filepath, destination)
                messagebox.showinfo("Success", "File moved successfully!")
            except Exception as e:
                messagebox.showerror("Error", "Failed to move file: " + str(e))
    else:
        messagebox.showerror("Error", "Please select a file and a destination folder.")

def open_file():
    global filepath
    if filepath:
        try:
            subprocess.Popen(['open', filepath]) # For macOS
        except:
            try:
                subprocess.Popen(['xdg-open', filepath]) # For Linux
            except:
                try:
                    os.startfile(filepath) # For Windows
                except Exception as e:
                    messagebox.showerror("Error", "Failed to open file: " + str(e))
    else:
        messagebox.showerror("Error", "Please select a file to open.")

def batch_rename():
    global folderpath
    if folderpath:
        pattern = simpledialog.askstring("Batch Rename", "Enter pattern for renaming (use # to represent index):")
        if pattern:
            files = os.listdir(folderpath)
            for i, file in enumerate(files):
                file_name, file_ext = os.path.splitext(file)
                new_file_name = pattern.replace("#", str(i+1))
                new_file_name = new_file_name + file_ext
                source = os.path.join(folderpath, file)
                destination = os.path.join(folderpath, new_file_name)
                if source != destination:
                    if os.path.exists(destination):
                        messagebox.showerror("Error", "File already exists in the folder. Please choose a different pattern.")
                    else:
                        try:
                            os.rename(source, destination)
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to rename file: " + str(e))
            messagebox.showinfo("Success", "Batch rename completed successfully!")
    else:
        messagebox.showerror("Error", "Please select a folder for batch renaming.")

frame = ttk.Frame(root)
frame.pack(pady=20)

file_label = ttk.Label(frame, text="Selected File: ")
file_label.grid(row=0, column=0, sticky=W, padx=10, pady=5)
folder_label = ttk.Label(frame, text="Selected Folder: ")
folder_label.grid(row=1, column=0, sticky=W, padx=10, pady=5)

browse_file_button = ttk.Button(frame, text="Browse File", command=browse_file)
browse_file_button.grid(row=0, column=1)

browse_folder_button = ttk.Button(frame, text="Browse Folder", command=browse_folder)
browse_folder_button.grid(row=1, column=1)

move_button = ttk.Button(frame, text="Move File", command=move_file)
move_button.grid(row=2, column=0, pady=10)

open_button = ttk.Button(frame, text="Open File", command=open_file)
open_button.grid(row=2, column=1, pady=10)

batch_rename_button = ttk.Button(frame, text="Batch Rename", command=batch_rename)
batch_rename_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
