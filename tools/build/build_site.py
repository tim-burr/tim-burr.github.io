# Imports
# System Utilities
import sys
from pathlib import Path
# Custom
from utils.drive_tools import *
from utils.config_loader import *
from utils.template_loader import *
from utils.generator import *

# Directories
CURR_DIR = Path(__file__).parent.resolve()
ROOT_DIR = Path(__file__).parents[2].resolve()

# Files
DEF_CONFIG = CURR_DIR / "config.yml" # Default

########################
# Main
########################
if __name__=="__main__":
    # Handle program inputs
    try:
        filepath = sys.argv[1]
    except IndexError:
        print("Empty or invalid configuration input... Using default")
        filepath = DEF_CONFIG

    # Load build config data
    config = configuration(ROOT_DIR, filepath)
    
    # Buffer filepaths from config data
    paths = config.get_paths()
    page_dir = paths.get("pages")
    build_dir = paths.get("build")

    # Remove old build directory, if exists
    delete_directory(build_dir)
    # Create new, empty build directory
    create_directory(build_dir)

    # Directly copy Includes into build directory
    includes = config.get_includes()
    for i, path in enumerate(includes):
        copy_recursive(includes[i], build_dir)

    # Initialize template lookup table
    templates = template(config)
    
    # Generate one HTML file per found Markdown file
    run = generator(config)

    website = page_dir.rglob("*.md")
    for page in website:
        run.generate(page, templates)

    print("\nWebsite generated!")