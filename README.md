# pypaths
A minimal, highly optimized path and temporary directory management utility for Python.

## Features:
- Path joining, creation, and validation.
- Lazy file loading to optimize memory usage.
- Temporary directory management with automatic cleanup.
- Singleton-based global path registration for large-scale projects.

## Installation:
Clone this repository, and add it to your Python project.

## Usage:
from path_utils import join_paths, create_project_path, LazyFileLoader, GlobalPathManager

# Join two paths
full_path = join_paths("/home/user/projects", "my_project")

# Create project directory
project_path = create_project_path("/home/user/projects", "my_project")

# Load a file lazily
lazy_loader = LazyFileLoader("config.json")
config_content = lazy_loader.read()  # File content is only read when `read()` is called

# Global path management
global_paths = GlobalPathManager()
global_paths.register_path("project", str(project_path))
project_path = global_paths.get_path("project")