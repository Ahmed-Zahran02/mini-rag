from .db_schema import Project
from .BaseDataModel import BaseDataModel
from .enums import DataBaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] # pyright: ignore[reportIndexIssue]

    async def create_project(self, project: Project) -> Project:
        project_dict = project.model_dump(by_alias=True, exclude_unset=True)
        result = await self.collection.insert_one(project_dict)
        # return the project with the assigned _id
        return project.model_copy(update={"_id": str(result.inserted_id)})

    async def get_project_or_create_one(self, project_id: str) -> Project:
        record = await self.collection.find_one({"_id": project_id})

        if record is None:
            project = Project(project_id=project_id)
            project = await self.create_project(project)
            return project

        return Project(**record)

    async def get_all_projects_in_page(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[Project], int]:
        cursor = self.collection.find().skip(page_size * (page - 1)).limit(page_size)

        projects = []
        async for doc in cursor:
            projects.append(Project(**doc))

        total_documents = await self.collection.count_documents({})
        total_pages = (total_documents + page_size - 1) // page_size

        return projects, total_pages
