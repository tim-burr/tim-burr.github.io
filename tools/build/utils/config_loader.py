# Imports
import yaml

# Script configuration manager
class configuration:
    def __init__(self, file):
        self._config = self._open_config(file)
    
    def _open_config(self, file):
        loaded = yaml.full_load(open(file, 'r'))
        print("Build configuration loaded")
        return loaded

    def _resolve_paths1(self, root, paths):
        # Prepend resolved file path to all config paths
        for key, value in paths.items():
            paths[key] = root / value 
        return paths

    def _resolve_paths2(self, root, paths):
        # Prepend resolved file path to all config paths
        for i, dir in enumerate(paths):
            paths[i] = root / dir
        return paths

    def get_config(self):
        return self._config

    def get_domain(self):
        return self._config.get("domain")

    def get_paths(self, root):
        rel_paths = self._config.get("paths")
        abs_paths = self._resolve_paths1(root, rel_paths)
        return abs_paths
        
    def get_includes(self, root):
        rel_includes = self._config.get("includes")
        abs_includes = self._resolve_paths2(root, rel_includes)
        return abs_includes

    def get_defaults(self):
        return self._config.get("defaults")