# Imports
import os
import shutil
from shutil import SameFileError
from pathlib import Path

def copy_file(src, dest):
    print(f"Copy: file {src} into {dest}")
    try:
        shutil.copy(src, dest) # Preserves meta data
    except SameFileError:
        print("Error: Source and destination are the same file.")
    except IsADirectoryError:
        print("Error: The destination is a directory.")

def copy_directory(src, dest):
    print(f"Copy: {src}\\ into {dest}\\")
    # Add try-catch path check here
    shutil.copytree(src, dest / Path(src).stem, dirs_exist_ok=True)

def copy_recursive(src, dest):
    print(f"Copy: {src}\\ into {dest}\\")
    # Add try-catch path check here
    shutil.copytree(src, dest, dirs_exist_ok=True)

def create_directory(dir):
    print(f"Create: directory {dir}\\")
    # Add try-catch path check here
    if not Path(dir).exists():
        os.makedirs(dir, exist_ok=True)
    
def delete_directory(dir):
    print(f"Remove: directory {dir}\\")
    # Add try-catch path check here
    if os.path.exists(dir):
        shutil.rmtree(dir)