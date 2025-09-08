from .BaseController import BaseController
from pathlib import Path


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, file_name: str) -> str:
        """Get the full path of a project given its name."""
        path = self.app_settings.DATA_DIR / file_name
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
