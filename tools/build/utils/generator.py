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
    def __init__(self, config: configuration):
        self._config = config
        self._paths = config.get_paths()
        self._templates = config.get_templates()
        self._includes = config.get_includes()
        self._pretty = config.get_pretty()
    
    def _parse_page(self, page):
        # Split YAML frontmatter from Markdown content
        with open(page) as f:
            # Buffer serialized page data
            metadata, content = frontmatter.parse(f.read())
        return metadata, content

    def _md_to_html(self, content):
        # Convert Markdown into HTML
        html = markdown.markdown(content)
        return html
        
    def generate(self, page):
        # Instance references
        build_dir = self._paths.get("build")
        template_dir = self._paths.get("templates")
        page_name = Path(page).stem  # Filename w/o extension

        # Exception: Homepage saves to build root
        # TODO: Find better way to implicitly handle this exception (YAML config item?)
        build_subdir = build_dir / page_name # Subdirectory name takes page name
        if page_name == "about":
            build_subdir = build_dir
        new_file = build_subdir / "index.html"

        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Convert Markdown into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

        # Open templates for token replacement
        open_templates = {}
        for template, path in self._templates.items():
            with open(template_dir / path, 'r', encoding='utf-8') as f:
                open_templates[template] = f.read()
        
        # TODO: Add logic for non-default templates
        html_doc = open_templates.get("default")

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
        # Adds new dict key/value if needed
        match metadata["category"]:
            case "about": params["{inactive_about}"] = "pure-menu-selected"
            case "project": params["{inactive_projects}"] = "pure-menu-selected"
            case "article": params["{inactive_articles}"] = "pure-menu-selected"

        # Customize tags in template buffer
        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key,value)
        
        # Prettify HTML (option)
        if self._pretty:
            html_doc = indent(html_doc)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print ("Page generated")