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
from utils.template_loader import *

class generator:
    def __init__(self, config: configuration):
        self._config = config
        self._paths = config.get_dict("paths")
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
        
    def generate(self, page, templates: template):
        # Instance references
        build_dir = self._paths.get("build")
        page_name = Path(page).stem  # Filename w/o extension

        # Convert custom page into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

        # Get page layout components from templates
        layouts = templates.get_files(metadata.get("template"))
        
        # Define recognized in-page template tags
        params = { # TODO: Make YAML configurable
            "{description}": metadata.get("description"),
            "{title}": metadata.get("title"),
            "{css}": metadata.get("css"), # TODO: Add logic for multiple CSS
            "{header}": layouts.get("header"),
            "{content}": html_content,
            "{footer}": layouts.get("footer"),
            "{media}": "media", # TODO: Make YAML configurable
            "{styles}": "styles" # TODO: Make YAML configurable
         }
        
        # Set active nav menu button
        # Adds new dict key/value pair if needed
        category = metadata["category"]
        try:
            params[f"{{inactive_{category}}}"] = "pure-menu-selected"
        except:
            print("No active menu links to update")

        # Customize tags in template buffer
        html_doc = layouts.get("content")

        for key, value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key, value)
        
        # Prettify HTML (compile option)
        if self._pretty:
            html_doc = indent(html_doc)
        
        # Determine final path of new page
        if page_name.isnumeric():
            # Numeric error page saves to build root
            build_subdir = build_dir
            new_file = (build_subdir / page_name).with_suffix(".html")
        elif page_name == self._homepage:
            # Homepage saves to build root
            build_subdir = build_dir
            new_file = build_subdir / "index.html"
        elif page_name == category:
            # Launch page saves near top of directory
            build_subdir = build_dir / page_name
            new_file = build_subdir / "index.html"
        else:
            # Default: Child page gets their own subfolder
            build_subdir = build_dir / category / page_name
            new_file = build_subdir / "index.html"
       
        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print("Page generated")