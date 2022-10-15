# Imports
# System Utilities
from pathlib import Path
# Document Parsers
import frontmatter
from markdown import markdown
from yattag import indent
# Custom
from utils.drive_tools import create_directory
from utils.config_loader import *

class generator:
    def __init__(self, config: configuration):
        self._config = config
        self._paths = config.get_dict("paths")
        self._templates = config.get_dict("templates", self._paths.get("templates"))
        self._homepage = config.get_homepage()
        self._pretty = config.get_pretty()
    
    def _parse_page(self, page):
        # Split serialized YAML frontmatter from Markdown content
        with open(page) as f:
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _md_to_html(self, content):
        # Convert Markdown into HTML
        html = markdown(content)
        return html
        
    def generate(self, page):
        # Instance references
        build_dir = self._paths.get("build")
        page_name = Path(page).stem  # Filename w/o extension

        # Convert custom page into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

        # Open all templates for token replacement
        # Note: Some efficiency is lost here for simplicity
        open_templates = {}
        for template, path in self._templates.items():
            with open(path, 'r', encoding='utf-8') as f:
                open_templates[template] = f.read()
        
        # Load overall page template
        # Check if default
        if metadata.get("template") == "default":
            html_doc = open_templates.get("default")
        # Else, search for requested template in page metadata
        else:
            for key, content in open_templates.items():
                if key == metadata.get("template") + ".html":
                    html_doc = content

        params = { # TODO: Make YAML configurable
            "{description}": metadata.get("description"),
            "{title}": metadata.get("title"),
            "{css}": metadata.get("css"), # TODO: Add logic for multiple CSS
            "{header}": open_templates.get("header"),
            "{content}": html_content,
            "{footer}": open_templates.get("footer"),
            "{media}": "media", # TODO: Make YAML configurable
            "{styles}": "styles" # TODO: Make YAML configurable
         }
        
        # Set active nav menu button
        # Adds new dict key/value pair if needed
        match metadata["category"]:
            case "about": params["{inactive_about}"] = "pure-menu-selected"
            case "project": params["{inactive_projects}"] = "pure-menu-selected"
            case "article": params["{inactive_articles}"] = "pure-menu-selected"

        # Customize tags in template buffer
        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key, value)
        
        # Prettify HTML (compile option)
        if self._pretty:
            html_doc = indent(html_doc)

        # Exception: Homepage saves to build root
        if page_name == self._homepage: 
            build_subdir = build_dir
        elif page_name == "404": # 404 page must be in root
            build_subdir = build_dir
        else:
            build_subdir = build_dir / page_name # Subdirectory name takes page name
       
        new_file = build_subdir / "index.html"

        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print ("Page generated")