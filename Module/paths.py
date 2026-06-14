import os
from pathlib import Path
from typing import Iterator, Optional


def with_caps_extensions(*extensions: str) -> set[str]:
    """Returns a set containing the given extensions as well as capitalized versions of each."""
    result = set(extensions)
    for extension in extensions:
        result.add(extension.upper())
    return result


def _children_with_extension(path: Path, *extensions: str) -> Iterator[Path]:
    if path.is_dir():
        all_extensions = with_caps_extensions(*extensions)
        for child in path.iterdir():
            if child.suffix in all_extensions:
                yield child


def children_with_extension(path: Path, *extensions: str) -> list[Path]:
    """Returns all the direct children of the given path having one of the given extensions."""
    return list(_children_with_extension(path, *extensions))


def child_with_extension(path: Path, *extensions: str) -> Optional[Path]:
    """Returns the first direct child of the given path having one of the given extensions."""
    return next(_children_with_extension(path, *extensions), None)


def walk_files_with_extension(path: Path, *extensions: str) -> Iterator[Path]:
    """Returns all children of the given path having one of the given extensions."""
    if path.is_dir():
        all_extensions = with_caps_extensions(*extensions)
        for root, dirs, files in os.walk(path):
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                if file_path.suffix in all_extensions:
                    yield file_path
