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
        template_dir = self._paths.get("templates")
        template_file = template_dir / "default.html" # TODO: Needs config file logic
        page_name = Path(page).stem  # Filename w/o extension
        build_dir = self._paths.get("build")
        media = self._paths.get("media")

        # Exception: Homepage saves to build root
        # TODO: Find better way to implicitly handle this exception (new frontmatter for landing page?)
        build_subdir = build_dir / page_name # Subdirectory name takes page name
        if page_name == "about":
            build_subdir = build_dir
        new_file = build_subdir / "index.html"

        # Create build subdirectory if it doesn't exist
        create_directory(build_subdir)

        # Convert Markdown into HTML
        metadata, content = self._parse_page(page)
        html_content = self._md_to_html(content)

        # Open Includes for template insertion
        with open(template_dir / "includes/header.html", 'r', encoding='utf-8') as f:
            header = f.read()
        with open(template_dir / "includes/footer.html", 'r', encoding='utf-8') as f:
            footer = f.read()
        # Buffer HTML template for parsing
        with open(template_file, 'r') as temp:
            html_doc = temp.read()

        params = { # TODO: Make YAML configurable
            "{description}": metadata.get("description"),
            "{title}": metadata.get("title"),
            "{css}": metadata.get("css"), # TODO: Add logic for multiple CSS
            "{header}": header,
            "{content}": html_content,
            "{footer}": footer,
            "{media}": "media",
            "{styles}": "styles",
         }
        
         # Set active nav menu button
         # Adds new dict key/value if needed
        match metadata["category"]:
            case "about": params["{inactive_about}"] = "pure-menu-selected"
            case "project": params["{inactive_projects}"] = "pure-menu-selected"
            case "article": params["{inactive_articles}"] = "pure-menu-selected"

        # Customize tags in template buffer
        for key,value in params.items():
            if key in html_doc:
                html_doc = html_doc.replace(key,value)
        
        # Prettify HTML (OPTIONAL)
        # TODO: Make YAML configurable (i.e. compile option)
        html_doc = indent(html_doc)

        # Save HTML buffer to new file
        with open(new_file, 'w') as f:
            f.write(html_doc)

        print ("Page generated")