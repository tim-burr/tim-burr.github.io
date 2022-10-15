# Imports
# System Utilities
from pathlib import Path
# Document Parsers
import markdown
import frontmatter
from yattag import indent
# Custom
from utils.drive_tools import *
from utils.config_loader import *

class generator:
    def __init__(self, root, config: configuration):
        self._config = config # TODO: Make better use of YAML config, not just for paths
        self._paths = config.get_paths(root)
        # TODO: Add additional initialized data stores
    
    def _parse_page(self, page):
        # Parse YAML frontmatter in open Markdown file
        with open(page) as reader:
            # Buffer all page data
            data = frontmatter.loads(reader.read())
        return data
        
    def _parse_frontmatter(self, data):
        # Split frontmatter
        params = {
            "description": data["description"],
            "title": data["title"],
            "css": data["css"], # Add logic for multiple CSS
            "category": data["category"]
        }
        return params

    def _convert_to_html(self, content):
        # Convert Markdown into HTML
        html = markdown.markdown(content)
        return html
        
    def generate(self, page):
        # Instance references
        template_dir = self._paths.get("templates")
        template_file = template_dir / "default.html" # TODO: Needs config file logic
        page_name = Path(page).stem  # Filename w/o extension
        build_dir = self._paths.get("build")
        media = self._paths.get("media")

        # Exception: Homepage saves to build root
        build_subdir = build_dir / page_name # Subdirectory name takes page name
        if page_name == "about":
            build_subdir = build_dir
        new_file = build_subdir / "index.html"

        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Convert Markdown into HTML
        data = self._parse_page(page)
        yaml = self._parse_frontmatter(data)
        content = self._convert_to_html(data.content) # Split content

        # Open Includes for template insertion
        with open(template_dir / "includes/header.html", 'r', encoding='utf-8') as f:
            header = f.read()
        with open(template_dir / "includes/footer.html", 'r', encoding='utf-8') as f:
            footer = f.read()
        # Buffer HTML template for parsing
        with open(template_file, 'r') as temp:
            html_doc = temp.read()

        params = { # TODO: Make YAML configurable
            "{description}": yaml.get("description"),
            "{title}": yaml.get("title"),
            "{header}": header,
            "{content}": content,
            "{footer}": footer,
            "{media}": "media",
            "{styles}": "styles",
         }
        
         # Set active nav menu button
         # Adds new dict key/value if needed
        match yaml["category"]:
            case "about": params["{inactive_about}"] = "pure-menu-selected"
            case "project": params["{inactive_projects}"] = "pure-menu-selected"
            case "article": params["{inactive_articles}"] = "pure-menu-selected"

        # Customize tags in template buffer
        for key,value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key,value)
        
        # Prettify HTML (OPTIONAL)
        html_doc = indent(html_doc)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print ("Page generated")