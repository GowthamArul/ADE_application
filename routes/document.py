from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Query
                     )

from sqlalchemy import (delete,
                        func,
                        inspect,
                        or_,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_db
from services.Documents.model_request import CreateDocumentRequest
from services.Documents.api import create_documents


router = APIRouter()

@router.post("",
             tags=["documents"],
             summary="Create Doucment")
async def create_documents(
    request:CreateDocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    
    
    pass