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

from database.base import get_db