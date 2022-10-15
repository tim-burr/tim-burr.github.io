# Imports
from pathlib import Path
# Custom
from utils.drive_tools import *

class template:
    def __init__(self, config):
        self._dir = Path(config.get_paths().get("templates"))
        self._filenames = walk_dir(self._dir)
        self._templates = {}
        self._open_essentials(config.get_templates(self._dir))

    # ****************
    # Private methods
    # ****************
    def _open_essentials(self, templates):
    # Open all essential templates for token replacement
        for name, path in templates.items():
            self._templates[name] = open_file(path)
        
    def _open_specific(self, filename):
    # Search if more specific template was requested
        content = ''
        try:
            path = self._filenames[filename]
            content = open_file(path)
        except:
            print("Using default template")
            content = self._templates["default"]
        return {'content': content} # Rename dict key to be standard no matter the page name

    # ****************
    # Public methods
    # ****************
    def get_files(self, filename):
        specific = self._open_specific(filename)
        return self._templates | specific # Return merged dict of all necessary templates