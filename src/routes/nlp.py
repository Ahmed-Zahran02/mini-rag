from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from .schemas import SearchRequest

from controllers import NLPController
from models import ChunkModel, ProjectModel, ResponseSignal

nlp_router = APIRouter(prefix="/v1/nlp")

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str):
    """Endpoint to index and push data into vectordb for a given project."""
    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROJECT_NOT_FOUND.value},
        )
    chunk_model = await ChunkModel.create_instance(request.app.state.db_client)

    nlp_controller = NLPController(request=request)
    page_no = 1
    idx = 0
    inserted_count = 0
    while True:
        chunks = await chunk_model.get_chunks_by_project_id(
            project_id=project.id, page_no=page_no
        )
        if not chunks or len(chunks) == 0:
            break
        chunk_ids = list(range(idx, len(chunks) + idx))
        idx += len(chunks)
        res = await nlp_controller.index_and_push(
            project=project,
            chunks=chunks,
            chunk_ids=chunk_ids,
        )

        if not res:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": ResponseSignal.INDEXING_FAILED.value},
            )
        inserted_count += len(chunks)
        page_no += 1

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": ResponseSignal.INDEXING_COMPLETED.value,
                "inserted_count": inserted_count,
            },
        )


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    """Endpoint to get index information for a given project."""
    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NLPController(request=request)

    info = await nlp_controller.get_index_info(project=project)

    return JSONResponse(
        content={
            "message": ResponseSignal.INDEX_INFO_RETRIEVED.value,
            "index_info": info,
        }
    )


@nlp_router.get("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, query: str):
    """Endpoint to search the vectordb for a given query in a project."""
    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NLPController(request=request)

    results = await nlp_controller.search_vectordb_collection(project=project, query=query)

    return JSONResponse(
        content={
            "message": ResponseSignal.SEARCH_COMPLETED.value,
            "results": results,
        }
    )


@nlp_router.post("/generate/answer/{project_id}")
async def generate_answer(
    request: Request, project_id: str, search_request: SearchRequest
):
    """Endpoint to generate answer based on the query and project context."""
    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    nlp_controller = NLPController(request=request)

    answer =await nlp_controller.generate_response(
        project=project, query=search_request.query
    )
    if not answer:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.GENERATION_FAILED.value},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseSignal.GENERATION_COMPLETED.value,
            "answer": answer,
        },
    )
