# Imports
import shutil
from pathlib import Path

def copy_file(src, dest):
    print(f"Copy: file {src} into {dest}")
    try:
        shutil.copy(src, dest) # Preserves meta data
    except shutil.SameFileError:
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
    if not Path(dir).exists(): # TODO: Check if this line is needed, if exist_ok exists. Same for other functions in this module.
        Path.mkdir(dir, parents=True, exist_ok=True)
    
def delete_directory(dir):
    print(f"Remove: directory {dir}\\")
    # Add try-catch path check here
    if Path(dir).exists():
        shutil.rmtree(dir)