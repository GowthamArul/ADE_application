from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    or_
)
import uuid
from database.chat import (DocumentModel, ArxivDetailModel)
from services.Documents.model_request import (CreateDocumentRequest, 
                                              ArxivDocs,
                                              CreateDocumentResponse)



async def create_documents(request:CreateDocumentRequest, db:AsyncSession):
    requested_documents_dict = {doc.document_name:doc for doc in request.documents}
    existing_documents = (await db.scalars(
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
        for _, document_name in enumerate(new_documents, start=1):
            try:
                requested_document = requested_documents_dict[document_name]
                document_model = DocumentModel(
                    document_id = uuid.uuid4(),
                    document_name = requested_document.document_name,
                    document_type = request.module,
                    title = requested_document.title
                )
                if request.module == "Arxiv":
                    assert isinstance(requested_document, ArxivDocs)
                    arxiv_doc = (
                        ArxivDetailModel(
                            arxiv_id = uuid.uuid4(),
                            summary = requested_document.summary,
                            publication_date = requested_document.publication_date,
                            updated_date = requested_document.updated_date,
                            link = requested_document.link,
                            authors = (str(requested_document.authors).replace(',', ' |') if requested_document.authors else "N/A"),
                        )
                    )
                    document_model.arxiv_details = arxiv_doc
                else:
                    raise Exception("Module not supported") from None
                new_document_models.append(document_model)
                db.add(document_model)
                await db.commit()
                return CreateDocumentResponse.model_validate(
                    {
                        'document_id_by_name': {doc.document_name: str(doc.document_id) for doc in new_document_models},
                        "created": len(new_document_models),
                        "existing": len(existing_doc_ids),
                        "status": "success"
                    }

                )

            except Exception as e:
                raise(f"Error: {e}")
    else:
        return CreateDocumentResponse.model_validate(
                    {
                        'document_id_by_name': {},
                        "created": 0,
                        "existing": len(existing_doc_ids),
                        "status": "success"
                    }

                )

