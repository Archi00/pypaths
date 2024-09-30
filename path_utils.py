from pathlib import Path
import os
import tempfile
from contextlib import contextmanager

# Core Path Utilities

def join_paths(*paths: str) -> Path:
    """Efficiently joins multiple paths and resolves to an absolute path."""
    return Path(*paths).resolve()

def create_directory(path: str) -> None:
    """Creates a directory (and parents if necessary) only if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def validate_path(path: str) -> bool:
    """Checks if a path exists."""
    return Path(path).exists()

# Temporary Directory Management

@contextmanager
def temporary_directory(prefix: str = "tmp_", suffix: str = "", dir: str = None):
    """Context manager for creating and cleaning up a temporary directory."""
    temp_dir = Path(tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=dir)).resolve()
    try:
        yield temp_dir
    finally:
        # Remove all files and directories within the temporary directory
        for item in temp_dir.iterdir():
            if item.is_dir():
                item.rmdir()
            else:
                item.unlink()
        temp_dir.rmdir()

# Lazy File Loading

class LazyFileLoader:
    """Lazily loads a file's content only when accessed to save memory."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._content = None

    def read(self) -> str:
        """Lazily reads and caches the file content."""
        if self._content is None:
            with self.file_path.open('r') as file:
                self._content = file.read()
        return self._content

# Path Factory for Projects and Temporary Paths

def create_project_path(base_path: str, project_name: str) -> Path:
    """Creates and returns the project's root directory path."""
    project_path = join_paths(base_path, project_name)
    create_directory(project_path)
    return project_path

def create_temp_path(prefix: str = "tmp_", suffix: str = "", base_path: str = None) -> Path:
    """Creates and returns a temporary directory for a project."""
    with temporary_directory(prefix, suffix, base_path) as temp_dir:
        return temp_dir

# Global Path Manager (Singleton)

class GlobalPathManager:
    """Singleton to globally manage registered paths."""
    
    _instance = None
    _paths = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_path(self, key: str, path: str) -> None:
        """Registers a path globally by key."""
        self._paths[key] = Path(path).resolve()

    def get_path(self, key: str) -> Path:
        """Retrieves a globally registered path by key."""
        return self._paths.get(key)
