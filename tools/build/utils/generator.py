# Imports
# System Utilities
from pathlib import Path
# Document Parsers
import frontmatter
from markdown import markdown
from yattag import indent
# Custom
from utils.drive_tools import *
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

        # Open all essential templates for token replacement
        essential_templates = {}
        for template, path in self._templates.items():
            with open(path, 'r', encoding='utf-8') as f:
                essential_templates[template] = f.read()
        
        # Set requested template as default, for now...
        html_doc = essential_templates.get("default")

        # Store dict of all files in template directory for later lookup
        all_templates = walk_dir(self._paths.get("templates"))

        # Search if more specific template was actually requested 
        try:
            real_template_path = all_templates[metadata.get("template")] 
            with open(real_template_path, 'r', encoding='utf-8') as f:
                html_doc = f.read()
        except:
            print("Using default template")

        params = { # TODO: Make YAML configurable
            "{description}": metadata.get("description"),
            "{title}": metadata.get("title"),
            "{css}": metadata.get("css"), # TODO: Add logic for multiple CSS
            "{header}": essential_templates.get("header"),
            "{content}": html_content,
            "{footer}": essential_templates.get("footer"),
            "{media}": "media", # TODO: Make YAML configurable
            "{styles}": "styles" # TODO: Make YAML configurable
         }
        
        # Set active nav menu button
        # Adds new dict key/value pair if needed
        try:
            match metadata["category"]:
                case "about": params["{inactive_about}"] = "pure-menu-selected"
                case "project": params["{inactive_projects}"] = "pure-menu-selected"
                case "article": params["{inactive_articles}"] = "pure-menu-selected"
        except:
            print("No active menu links to update")

        # Customize tags in template buffer
        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key, value)
        
        # Prettify HTML (compile option)
        if self._pretty:
            html_doc = indent(html_doc)

        # TODO: Remove if-elif. Make generic based on directory structure.
        # Exception: Homepage saves to build root
        if page_name == self._homepage:
            build_subdir = build_dir
            new_file = build_subdir / "index.html"
        # Exception: Error page saves to build root
        elif page_name == "404":
            build_subdir = build_dir
            new_file = build_subdir / "404.html"
        # Exception: Launch pages live near top of directory
        elif page_name == metadata["category"]:
            build_subdir = build_dir / page_name
            new_file = build_subdir / "index.html"
        # Else, child pages get their own subfolder
        else:
            build_subdir = build_dir / metadata["category"] / page_name
            new_file = build_subdir / "index.html"
       
        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print ("Page generated")