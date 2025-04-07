from pydantic import BaseModel
from pydantic import Field
import uuid



class CreateCollectionRequest(BaseModel):
    collection_id: str | None = None
    document_ids: list[str]
    collection_name: str | None = None
    collection_description: str | None = None
    user_id: str
    module_name: str
    session_name: str | None = None

class CreateCollectionResponse(BaseModel):
    collection_id : str
    collection_status: str
    message: str
    chat_session_id: str | None
    