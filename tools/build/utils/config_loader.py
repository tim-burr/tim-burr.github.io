# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, root, file):
        self._config = self._open_config(file)
        self._root = root
    
    def _open_config(self, file):
        loaded = yaml.full_load(open(file, 'r'))
        print("Build configuration loaded")
        return loaded

    def _resolve_paths_dict(self, paths):
        # Prepend resolved file path to all config paths
        for key, value in paths.items():
            paths[key] = self._root / value 
        return paths

    def _resolve_paths_list(self, paths):
        # Prepend resolved file path to all config paths
        for i, dir in enumerate(paths):
            paths[i] = self._root / dir
        return paths

    def get_config(self):
        return self._config

    def get_domain(self):
        return self._config.get("domain")

    def get_paths(self):
        rel_paths = self._config.get("paths")
        abs_paths = self._resolve_paths_dict(rel_paths)
        return abs_paths
    
    def get_templates(self):
        rel_templates = self._config.get("templates")
        abs_templates = self._resolve_paths_dict(rel_templates)
        return abs_templates

    def get_includes(self):
        rel_includes = self._config.get("includes")
        abs_includes = self._resolve_paths_list(rel_includes)
        return abs_includes

    def get_pretty(self):
        return self._config.get("html_pretty")