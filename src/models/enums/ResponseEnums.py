from enum import Enum


class ResponseSignal(Enum):
    FILE_VALID = "File validated successfully"
    FILE_INVALID_TYPE = "File type not allowed"
    FILE_INVALID_SIZE = "File size exceeds maximum allowed size"
    FILE_NO_NAME = "Filename is required"
    FILE_SIZE_UNDETERMINED = "File size could not be determined"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILURE = "File upload failed"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_NOT_FOUND = "File not found"
    PROCESSING_SUCCESS = "File processed successfully"
    PROCESSING_FAILURE = "File processing failed"
    PROJECT_NOT_FOUND = "Project not found"
    INDEXING_FAILED = "Indexing failed"
    INDEXING_COMPLETED = "Indexing completed successfully"
    INDEX_INFO_RETRIEVED = "Index information retrieved successfully"
    SEARCH_COMPLETED = "Search completed successfully"
    GENERATION_FAILED = "Response generation failed"
    GENERATION_COMPLETED = "Response generated successfully"
