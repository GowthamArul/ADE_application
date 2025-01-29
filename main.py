from contextlib import asynccontextmanager
import logging
from fastapi import (FastAPI, Request)
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
import time
from configs.config import DB_SCHEMA
from database.base import engine
from sqlalchemy.schema import CreateSchema


from scripts import *
from database.chat import JarvisBase



init_logger()

@asynccontextmanager
async def lifespan(app:FastAPI):
    if DB_SCHEMA and DB_SCHEMA != 'public':
        async with engine.connect() as conn:
            await conn.execute(CreateSchema(DB_SCHEMA, if_not_exists=True))
            await conn.commit()
    async with engine.begin() as conn:
        await conn.run_sync(JarvisBase.metadata.create_all)
    yield

app = FastAPI(
    title='Patient Data Management',
    description="The PDM application will help maintain patients' historical medication records and allow doctors to chat with an LLM model to gain insights about the drugs.",
    version= "1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)

app.middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

