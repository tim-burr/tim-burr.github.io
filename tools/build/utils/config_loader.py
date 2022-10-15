# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, root, file):
        self._root = root
        self._config = self._open_config(file)
    
    def _open_config(self, file):
        loaded = yaml.safe_load(open(file, 'r'))
        print("Build configuration loaded")
        return loaded

    def get_config(self):
        return self._config

    def get_domain(self):
        return self._config.get("domain")

    def get_tokens(self):
        pass

    def get_homepage(self):
        return self._config.get("homepage")

    def get_pretty(self):
        return self._config.get("html_pretty")

    def get_dict(self, key: str, base = ''):
        paths = self._config.get(key)
        # Resolve all relative file paths
        for index, value in paths.items():
            paths[index] = self._root / base / value 
        return paths

    def get_list(self, key: str, base = ''):
        paths = self._config.get(key)
        # Resolve all relative file paths
        for index, value in enumerate(paths):
            paths[index] = self._root / base / value
        return paths