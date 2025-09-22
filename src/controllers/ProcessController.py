from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain.document_loaders import TextLoader, PyMuPDFLoader
from models import ProcessingType, ResponseSignal


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_controller = ProjectController()
        self.project_id = project_id
        self.project_path = self.project_controller.get_project_path(
            file_name=project_id
        )

    def get_file_extension(self, file_name: str) -> str:
        return os.path.splitext(file_name)[-1].lower()

    def get_file_loader(self, file_path: str):
        file_extension = self.get_file_extension(file_path)
        if file_extension == ProcessingType.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingType.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value)

    def process_file(self, file_id: str):
        file_path = os.path.join(self.project_path, file_id)
        if not os.path.exists(file_path):
            return None, ResponseSignal.FILE_NOT_FOUND.value
        try:
            loader = self.get_file_loader(file_path)
            documents = loader.load()
            return documents, ResponseSignal.PROCESSING_SUCCESS.value
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, str(e)
