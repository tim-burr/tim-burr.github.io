# Imports
# System Utilities
import sys
from pathlib import Path
# Custom
from utils.drive_tools import *
from utils.config_loader import *
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
    config = configuration(filepath)
    
    # Look up Includes
    includes = config.get_includes(ROOT_DIR)

    # Buffer filepaths from config data
    paths = config.get_paths(ROOT_DIR)
    page_dir = paths.get("pages")
    build_dir = paths.get("build")

    # Remove build directory (fresh build)
    delete_directory(build_dir)
    # Create empty build directory to start
    create_directory(build_dir)
    # Direct copy includes into build directory
    for i, path in enumerate(includes):
        copy_recursive(includes[i], build_dir)

    # Generate one HTML file per found Markdown file
    run = generator(ROOT_DIR, config) # TODO: Simplify class instantiation without ROOT_DIR passed in?

    website = page_dir.rglob("*.md")
    for page in website:
        run.generate(page)

    print("\nWebsite generated!")