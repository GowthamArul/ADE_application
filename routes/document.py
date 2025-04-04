from fastapi import (APIRouter,
                     Depends,
                     )

from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_db
from services.Documents.model_request import (CreateDocumentRequest,
                                              CreateDocumentResponse)
from services.Documents.api import create_documents


router = APIRouter()

@router.post("",
             tags=["documents"],
             summary="Create Doucment",
             response_model=CreateDocumentResponse)
async def create_documents_api(
    request:CreateDocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    return await create_documents(request, db)
    