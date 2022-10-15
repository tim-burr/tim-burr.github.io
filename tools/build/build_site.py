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
        print("Invalid configuration input... Using default.")
        filepath = DEF_CONFIG

    # Load build config data
    config = configuration(filepath)
    
    # Buffer filepaths from config data
    paths = config.get_paths(ROOT_DIR)
    page_dir = paths.get("pages")
    style_dir = paths.get("styles")
    media_dir = paths.get("media")
    build_dir = paths.get("build")

    # Remove build directory (fresh build)
    delete_directory(build_dir)
    # Create build directory
    create_directory(build_dir)
    # Establish custom domain
    copy_file(ROOT_DIR / "_data/CNAME", build_dir) # TODO: Loop on copying everything in _data dir
    copy_file(ROOT_DIR / "_data/sitemap.xml", build_dir)
    copy_file(ROOT_DIR / "_data/robots.txt", build_dir)
    # Build page styles
    copy_directory(style_dir, build_dir) # TODO: Make below copy_dir calls extensible based on config assets (loop?)
    # Build media
    copy_directory(media_dir, build_dir)

    run = generator(ROOT_DIR, config) # TODO: Simplify class instantiation without ROOT_DIR passed in?

    # Generate one HTML file per found Markdown file
    website = page_dir.rglob("*.md")
    for page in website:
        run.generate(page)

    print("\nWebsite generated!")