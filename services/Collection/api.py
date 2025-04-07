from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    func
)
import uuid
from database.chat import (CollectionModel,
                           DocumentModel,
                           ChatSessionModel)
from .schemas import CreateCollectionRequest, CreateCollectionResponse

import traceback

logger = getLogger(__name__)

async def create_collection(request:CreateCollectionRequest, db:AsyncSession) -> CreateCollectionResponse:
    try:
        if request.module_name == 'Arxiv':
            if not request.collection_id:
                collection = CollectionModel(
                    collection_id = uuid.uuid4(),
                    collection_name = request.collection_name,
                    description = request.collection_name,
                    user_id = request.user_id,
                    module_name = request.module_name
                )
                db.add(collection)
                list_of_documents = request.document_ids
            else:
                collection = await db.scalar(
                    select(CollectionModel).where(
                        CollectionModel.collection_id == request.collection_id
                    )
                )
                if not collection:
                    return CreateCollectionResponse(
                        collection_id = "",
                        collection_status = "",
                        message = 'Collection not found',
                        chat_session_id = ""
                    )
                docs_in_collection = [document.document_name for document in collection.documents if document.document_name in request.document_ids]
                list_of_documents = list(set(request.document_ids) - set(docs_in_collection))
                if not list_of_documents:
                    return CreateCollectionResponse(
                        collection_id = str(collection.collection_id),
                        collection_status = "ACTIVE",
                        message = 'Documents already in collection',
                        chat_session_id = ""
                    )
            subquery_1 = (
                select(DocumentModel.document_name)
                .group_by(DocumentModel.document_name)
                .having(func.count(DocumentModel.document_name) > 1)
                .subquery()
            )

            multuple_docs = (
                select(DocumentModel)
                .join(
                    subquery_1,
                    DocumentModel.document_name == subquery_1.c.document_name
                )
                .filter(
                    DocumentModel.document_name.in_(list_of_documents),
                    DocumentModel.file_id.is_(None),
                )
            )

            subquery_2 = (
                select(DocumentModel.document_name)
                .group_by(DocumentModel.document_name)
                .having(func.count(DocumentModel.document_name) == 1)
                .subquery()
            )

            unique_docs = (
                select(DocumentModel)
                .join(
                    subquery_2,
                    DocumentModel.document_name == subquery_2.c.document_name
                )
                .filter(
                    DocumentModel.document_name.in_(list_of_documents)
                )
            )

            final_query = multuple_docs.union(unique_docs)

            result_ls = (await db.execute(final_query)).scalars().all()
            doc_ids_ls = [i for i in result_ls]
            results = (await db.execute(
                select(DocumentModel).filter(
                    DocumentModel.document_id.in_(doc_ids_ls)
                )
            )).scalars().all()

            collection.documents.extend(results)

            # Clara Code base for embeddings
            # ---> In-progress
            ######

            logger.info(f"Created New Collection: collection_id = {collection.collection_id}")
            db.add(collection)
            existing_session = (
                await db.scalars(
                    select(ChatSessionModel).where(
                        ChatSessionModel.collection_id == collection.collection_id,
                        ChatSessionModel.status == "ACTIVE",
                    )
                )
            ).all()
            if existing_session:
                for session in existing_session:
                    session.status = "LOCKED"
                    logger.info(f"Locked {len(existing_session)} existing sessions")
                await db.commit()
            else:
                logger.info("No existing sessions found")
                await db.commit()
            
            return CreateCollectionResponse(
                        collection_id = str(collection.collection_id),
                        collection_status = "ACTIVE",
                        message = 'Documents added to the collection',
                        chat_session_id = ""
                    )
    except Exception as ex:
        return CreateCollectionResponse(
                        collection_id = "",
                        collection_status = "",
                        message = f"Error: {ex}",
                        chat_session_id = ""
                    )       