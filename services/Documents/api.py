from sqlalchemy.ext.asyncio import AsyncSession
from services.Documents.model_request import CreateDocumentRequest


async def create_documents(request:CreateDocumentRequest, db:AsyncSession):
    requested_documents_dict = {doc.document_name:doc for doc in request.documents}
    pass