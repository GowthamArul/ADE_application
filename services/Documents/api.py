from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    or_
)
from database.chat import (DocumentModel)
from services.Documents.model_request import CreateDocumentRequest



async def create_documents(request:CreateDocumentRequest, db:AsyncSession):
    requested_documents_dict = {doc.document_name:doc for doc in request.documents}
    print(requested_documents_dict)
    existing_documents = (await db.execute(
        select(DocumentModel.document_name)
        .where(DocumentModel.document_name.in_(requested_documents_dict.keys()))
        .where(
            or_(
                DocumentModel.user_id == request.user_id,
                DocumentModel.user_id.is_(None),
                DocumentModel.user_id == "",
            )
        ).distinct()
    )).all()
    
    existing_doc_ids = set([str(x) for x in existing_documents])
    new_documents = set(requested_documents_dict.keys()) - existing_doc_ids

    new_document_models : list[DocumentModel] =[]

    if new_documents:
        for count, document_name in enumerate(new_documents, start=1):
            print(count, document_name)
