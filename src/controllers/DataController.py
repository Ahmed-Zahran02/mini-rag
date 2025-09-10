from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):
    size_scale = 1024 * 1024  # 1 MB

    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
        """Validate uploaded file and return specific error message if invalid."""
        if file.size is None:
            return (False, ResponseSignal.FILE_SIZE_UNDETERMINED.value)

        if not file.filename:
            return (False, ResponseSignal.FILE_NO_NAME.value)

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return (
                False,
                ResponseSignal.FILE_INVALID_TYPE.value,
            )

        max_size_bytes = self.app_settings.FILE_MAX_SIZE * self.size_scale
        if file.size > max_size_bytes:
            return (
                False,
                ResponseSignal.FILE_INVALID_SIZE.value,
            )

        return True, ResponseSignal.FILE_VALID.value

    def clean_file_name(self, filename: str) -> str:
        """Clean the filename by removing unwanted characters."""
        # Remove any character that is not alphanumeric, a dot, or hyphen
        cleaned_name = re.sub(r"[^\w.]", "", filename.strip())
        cleaned_name = cleaned_name.replace(" ", "_")
        return cleaned_name

    def generate_unique_filepath(self, original_filename: str, file_name: str):
        """Generate a unique filename by appending a random string to the original filename."""
        project_path = ProjectController().get_project_path(
            file_name=file_name
        )  # Get base project path
        random_string = self.generate_random_string(8)
        cleaned_name = self.clean_file_name(original_filename)
        new_filepath = os.path.join(project_path, f"{random_string}_{cleaned_name}")
        while os.path.exists(new_filepath):
            random_string = self.generate_random_string(8)
            new_filepath = os.path.join(project_path, f"{random_string}_{cleaned_name}")
        unique_filepath = new_filepath
        return unique_filepath, random_string + "_" + cleaned_name
