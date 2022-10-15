# Imports
import shutil
from pathlib import Path

def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.SameFileError:
        print("Error: Source and destination are the same file.")
        return False
    except IsADirectoryError:
        print("Error: The destination is a directory.")
        return False
    print(f"Copy: file {src} into {dest}")

def copy_directory(src, dest):
    print(f"Copy: {src}\\ into {dest}\\")
    shutil.copytree(src, dest / Path(src).stem, dirs_exist_ok=True)

def copy_recursive(src, dest):
    print(f"Copy: {src}\\ into {dest}\\")
    shutil.copytree(src, dest, dirs_exist_ok=True)

def create_directory(dir):
    print(f"Create: directory {dir}\\")
    Path.mkdir(dir, parents=True, exist_ok=True)
    
def delete_directory(dir):
    if Path(dir).exists():
        print(f"Remove: directory {dir}\\")
        shutil.rmtree(dir)