from inspect import ArgInfo
import os
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers import Settings, get_settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemas import DataSchema

data_router = APIRouter(prefix="/v1/data")
# add logging configuration to show only error messages
logger = logging.getLogger("uvicorn.error")


## Endpoint to upload a file
@data_router.post("/upload/{project_id}")
async def upload_file(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()
    result, signal = data_controller.validate_uploaded_file(file=file)

    if not result:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": signal},
        )
    # Save the file to the specified directory
    project_path = ProjectController().get_project_path(file_name=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        original_filename=file.filename, file_name=project_id
    )

    # Write the file in chunks to avoid memory issues with large files
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(app_settings.CHUNK_SIZE):
                await out_file.write(content)
    except Exception as e:
        logger.error(f"Error saving file {file.filename}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.FILE_UPLOAD_FAILURE.value},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
        },
    )


## Endpoint to process a file
@data_router.post("/process/{project_id}")
async def process_file(project_id: str, data_schema: DataSchema):
    process_controller = ProcessController(project_id=project_id)
    file_content, signal = process_controller.get_file_content(
        file_id=data_schema.file_id
    )
    if not file_content:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": signal},
        )
    try:
        chunks = process_controller.process_file(
            file_content=file_content,
            file_id=data_schema.file_id,
            chunk_size=data_schema.chunk_size,
            chunk_overlap=data_schema.overlap,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": ResponseSignal.PROCESSING_SUCCESS.value,
                "chunks": [chunk.dict() for chunk in chunks],
            },
        )
    except Exception as e:
        logger.error(f"Error processing file {data_schema.file_id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.PROCESSING_FAILURE.value},
        )
    