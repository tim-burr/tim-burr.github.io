# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, root, file):
        self._root = root
        self._config = self._open_config(file)
    
    # ****************
    # Private methods
    # ****************
    def _open_config(self, file):
        with open(file, 'r') as f:
            loaded = yaml.safe_load(f)
        print("Build configuration loaded")
        return loaded

    def _get_dict(self, key: str, base = ''):
        paths = self._config.get(key)
        # Resolve all relative file paths
        for index, value in paths.items():
            paths[index] = self._root / base / value 
        return paths

    def _get_list(self, key: str, base = ''):
        paths = self._config.get(key)
        # Resolve all relative file paths
        for index, value in enumerate(paths):
            paths[index] = self._root / base / value
        return paths
    
    # ****************
    # Public methods
    # ****************
    def get_config(self):
        return self._config

    def get_domain(self):
        return self._config.get("domain")

    def get_homepage(self):
        return self._config.get("homepage")

    def get_paths(self):
        return self._get_dict("paths")
    
    def get_templates(self, path = ''):
        return self._get_dict("templates", path)

    def get_includes(self, path = ''):
        return self._get_list("includes", path)

    def get_tokens(self):
        return self._config.get("tokens")

    def get_pretty(self):
        return self._config.get("html_pretty")