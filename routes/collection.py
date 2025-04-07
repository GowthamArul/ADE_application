from fastapi import (APIRouter,
                     Depends,
                     )

from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_db
from services.Collection.schemas import (CreateCollectionRequest,
                                              CreateCollectionResponse)
from services.Collection.api import create_collection


router = APIRouter()

@router.post("",
             tags=["Collection"],
             summary="Create Collection",
             response_model=CreateCollectionResponse)
async def create_documents_api(
    request:CreateCollectionRequest,
    db: AsyncSession = Depends(get_db)
):
    return await create_collection(request, db)