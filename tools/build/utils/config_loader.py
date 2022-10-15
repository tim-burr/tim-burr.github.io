# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, root, file):
        print(file)
        self._config = self._open_config(file)
        self._root = root
    
    def _open_config(self, file):
        loaded = yaml.safe_load(open(file, 'r'))
        print("Build configuration loaded")
        return loaded

    def _resolve_paths_dict(self, base, paths: dict):
        # Prepend resolved file path to all config paths
        for key, value in paths.items():
            paths[key] = base / value 
        return paths

    def _resolve_paths_list(self, base, paths: list):
        # Prepend resolved file path to all config paths
        for i, dir in enumerate(paths):
            paths[i] = base / dir
        return paths

    def get_config(self):
        return self._config

    def get_domain(self):
        return self._config.get("domain")

    # TODO: Refactor below to a single function "get_dict(self, base, key)"
    def get_paths(self):
        rel_paths = self._config.get("paths")
        abs_paths = self._resolve_paths_dict(self._root, rel_paths)
        return abs_paths

    def get_templates(self, base = ''):
        rel_paths = self._config.get("templates")
        abs_paths = self._resolve_paths_dict(self._root / base, rel_paths)
        return abs_paths

    def get_includes(self, base = ''):
        rel_paths = self._config.get("includes")
        abs_paths = self._resolve_paths_list(self._root / base, rel_paths)
        return abs_paths

    def get_tokens(self):
        pass

    def get_pretty(self):
        return self._config.get("html_pretty")