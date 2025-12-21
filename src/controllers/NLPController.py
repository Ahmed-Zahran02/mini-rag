from logging import Logger

from bson import ObjectId
from fastapi import Request

from models.db_schema import DataChunk, Project
from stores.llm.LLMEnums import DocumentTypes
from stores.llm.LLMExceptions import EmbeddingException

from .BaseController import BaseController


class NLPController(BaseController):
    def __init__(self, request: Request):
        super().__init__()
        self.embedding_client = request.app.state.embedding_client
        self.vectordb_client = request.app.state.vectordb_client
        self.generation_client = request.app.state.generation_client
        self.template_parser = request.app.state.template_parser
        self.logger = Logger("NLPController")

    async def index_and_push(
        self, project: Project, chunks: list[DataChunk], chunk_ids: list[int]
    ) -> bool:
        """Indexes and pushes data into the vector database for a given project."""
        try:
            texts = [chunk.chunk_content for chunk in chunks]
            metadatas = [
                {**chunk.chunk_metadata, "content": chunk.chunk_content}
                for chunk in chunks
            ]
            vectors = [self.embedding_client.embed_text(text=text) for text in texts]
            flag = self.vectordb_client.create_collection(
                collection_name=project.project_id
            )
            if not flag:
                self.logger.error(
                    f"Failed to create collection for project {project.project_id}"
                )
                return False

            _ = self.vectordb_client.insert_many(
                collection_name=project.project_id,
                vectors=vectors,
                metadatas=metadatas,
                ids=[str(ObjectId()) for _ in chunk_ids],
            )
            return True
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            return False

    async def get_index_info(self, project: Project) -> dict:
        """Retrieves index information for a given project."""
        try:
            collection_info = self.vectordb_client.get_collection_info(
                collection_name=project.project_id
            )
            if not collection_info:
                raise ValueError(f"Collection {project.project_id} not found")
            return collection_info
        except Exception as e:
            self.logger.error(f"Error retrieving index info: {e}")
            return {}

    async def search_vectordb_collection(
        self, project: Project, query: str, limit: int = 3
    ):
        """Searches the vector database collection for a given project using a query."""
        vector = self.embedding_client.embed_text(
            text=query, input_type=DocumentTypes.DOCUMENT.value
        )
        if vector is None or len(vector) == 0:
            raise EmbeddingException("Embedding returned empty vector.")

        res = self.vectordb_client.search_by_vector(
            collection_name=project.project_id, vector=vector, limit=limit
        )
        if res is None:
            raise Exception(
                f"Vector DB search failed for collection: {project.project_id}"
            )
        return res

    async def generate_response(self, project: Project, query: str, limit: int = 3):
        """Generates a response using the generation model for a given prompt."""
        docs = await self.search_vectordb_collection(project, query, limit)

        if not docs:
            self.logger.error("No documents found in vector database.")
            return None

        # construct prompt
        sys_prompt = self.template_parser.get_template("rag", "system_prompt", {})
        doc_prompt = "/n".join(
            [
                self.template_parser.get_template(
                    "rag",
                    "document_prompt",
                    {"doc_number": i + 1, "doc_content": doc.text},
                )
                for i, doc in enumerate(docs)
            ]
        )
        footer_prompt = self.template_parser.get_template(
            "rag", "footer_prompt", {"query": query}
        )

        chat_history = [
            self.generation_client.construct_prompt(role="system", content=sys_prompt),
        ]
        full_prompt = "/n".join([doc_prompt, footer_prompt])
        response = self.generation_client.generate_text(
            prompt=full_prompt, max_tokens=256, history=chat_history
        )
        return response, full_prompt, chat_history
