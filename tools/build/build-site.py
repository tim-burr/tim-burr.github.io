# Imports
# System Utilities
import os
import shutil
from pathlib import Path
# Document Parsers
import markdown
import yaml
import frontmatter
# Custom


# Directories
ROOT_DIR = Path(__file__).parents[2].resolve()
CONFIG_DIR = ROOT_DIR / "_data"
# Files
DEFAULT_CONFIG = CONFIG_DIR / "config.yml"
CNAME = ROOT_DIR / "CNAME"


# Functions
def open_config(file):
    config = yaml.full_load(open(file, 'r'))
    print("Build configuration loaded")
    return config


def get_paths(config):
    paths = config["paths"]
    # Prepend resolved file path to all config paths
    for key, value in paths.items():
        paths[key] = ROOT_DIR / value 
    return paths


def get_defaults(config):
    return config["defaults"]


def get_includes(config):
    return config["includes"]


def clear_directory(dir):
    # Add try-catch path check here
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print("Build directory cleared")


def copy_directory(src, dest):
    # Add try-catch path check here
    shutil.copytree(src, dest / Path(src).stem)
    print(f"Copied {src} into build directory")


def copy_file(src, dest):
    # Add try-catch path check here
    shutil.copy(src, dest)
    print(f"Copied {src} into build directory")


def generate(page, paths):
    # Temporary filepaths
    template_file = paths["templates"] / "default.html" # TODO: Needs config file logic
    page_name = Path(page).stem  # Filename w/o extension
    build_dir = paths["build"]
    build_subdir = build_dir / page_name # Subdirectory name takes page name
    media = paths["media"]

    # Exception: Homepage saves to build root
    if page_name == "about":
        build_subdir = build_dir 
    new_file = build_subdir / "index.html"
    
    # Create build subdirectory if it doesn't exist
    # Add try-catch path check here
    if not Path(build_subdir).exists():
        os.makedirs(build_subdir)

    # Parse YAML frontmatter in open Markdown file
    with open(page) as reader:
        # Buffer all page data
        data = frontmatter.loads(reader.read())
    
    # Split content
    md_content = data.content
      # Convert Markdown into HTML
    html_content = markdown.markdown(md_content)
    # Split frontmatter
    description = data["description"]
    title = data["title"]
    css = data["css"] # Add logic for multiple CSS
    category = data["category"]

    # Open Includes for template insertion
    with open(paths["templates"]/"includes/header.html", 'r', encoding='utf-8') as f:
        header = f.read()
    with open(paths["templates"]/"includes/footer.html", 'r', encoding='utf-8') as f:
        footer = f.read()
    # Buffer HTML template for parsing
    with open(template_file, 'r') as temp:
        html_doc = temp.read()

    # USE THIS AS A REPLACEMENT VALUE FOR "ACTIVE" KEY
    #pure-menu-selected

    pairs = { # Make YAML configurable
        "{description}": description,
        "{title}": title,
        "{header}": header,
        "{content}": html_content,
        "{footer}": footer,
        "{media}": "media",
        "{styles}": "styles",
    }
    # Set active nav menu button
    match category:
        case "about": pairs["{inactive_about}"] = "pure-menu-selected"
        case "project": pairs["{inactive_projects}"] = "pure-menu-selected"
        case "article": pairs["{inactive_articles}"] = "pure-menu-selected"

    # Customize tags in template buffer
    for key,value in pairs.items():
        if key in html_doc:
            html_doc = html_doc.replace(key,value)
    
    # Save HTML buffer to new file
    with open(new_file, 'w') as f:
        f.write(html_doc)

    print ("Page generated")


########################
# Main
########################
# Load build config data
def_config = open_config(DEFAULT_CONFIG)

# Buffer filepaths from config data
paths = get_paths(def_config)
templates_dir = paths["templates"]
pages_dir = paths["pages"]
styles_dir = paths["styles"]
media_dir = paths["media"]
build_dir = paths["build"]

# Clear outputs folder before new build
clear_directory(build_dir)
# Build page styles
copy_directory(styles_dir, build_dir)
# Build media
copy_directory(media_dir, build_dir)
# Establish custom domain
copy_file(CNAME, build_dir)

# Generate one HTML file per found Markdown file
website = pages_dir.rglob("*.md")
for page in website:
    generate(page, paths)

print("Website generated!")