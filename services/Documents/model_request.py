from pydantic import BaseModel
from pydantic import Field
import uuid


class SourceDocument(BaseModel):
    document_id: str = Field(
        validate_default=lambda: str(uuid.uuid4()),
        description="Global Unique identifier for the document"
    )
    document_name: str
    title: str
    text:str | None = None

class ArxivDocs(SourceDocument):
    id: str
    authors: str
    summary: str
    primary_category: str
    secondary_categories: str
    publication_date: str
    updated_date: str | None = None
    link: str | None = None
    

class CreateDocumentRequest(BaseModel):
    documents: list[ArxivDocs]
    user_id:str
    module: str = "Arxiv"

class CreateDocumentResponse(BaseModel):
    document_id_by_name: dict[str, str]
    created: int
    existing: int
    status: str