# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, file):
        self._config = self.open_config(file)
    
    def open_config(self, file):
        loaded = yaml.full_load(open(file, 'r'))
        print("Build configuration loaded")
        return loaded

    def get_config(self):
        return self._config

    def get_paths(self, root):
        paths = self._config["paths"]
        # Prepend resolved file path to all config paths
        for key, value in paths.items():
            paths[key] = root / value 
        return paths

    def get_defaults(self):
        return self._config["defaults"]

    def get_includes(self):
        return self._config["includes"]