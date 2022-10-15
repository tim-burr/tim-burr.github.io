# Imports
import os
import shutil
from pathlib import Path

def copy_file(src, dest):
    print(f"Copy: {src} into {dest}")
    # Add try-catch path check here
    shutil.copy(src, dest)

def create_directory(dir):
    print(f"Create: directory {dir}")
    # Add try-catch path check here
    if not Path(dir).exists():
        os.makedirs(dir)

def copy_directory(src, dest):
    print(f"Copy: {src} into {dest}")
    # Add try-catch path check here
    shutil.copytree(src, dest / Path(src).stem)

def delete_directory(dir):
    print(f"Remove: {dir}")
    # Add try-catch path check here
    if os.path.exists(dir):
        shutil.rmtree(dir)