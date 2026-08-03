"""
Compatibility patches for third-party libraries.

Import this module before importing kh2fmbr/khbr.
"""
import yaml

# kh2fmbr calls yaml.load without a Loader, which PyYAML 6 no longer allows.
# Make bare yaml.load default to SafeLoader (PyYAML 5.x used FullLoader with a
# warning; the data files involved are plain YAML, so SafeLoader suffices).
if not getattr(yaml, "_kh2rando_load_patched", False):
    _original_load = yaml.load

    def _load_with_default_loader(stream, Loader=None):
        return _original_load(stream, Loader=Loader or yaml.SafeLoader)

    yaml.load = _load_with_default_loader
    yaml._kh2rando_load_patched = True
