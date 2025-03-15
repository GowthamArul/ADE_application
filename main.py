from contextlib import asynccontextmanager
import logging
import uvicorn
from fastapi import (FastAPI, Request)
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, Response
import traceback
import time
from configs.config import DB_SCHEMA
from database.base import engine
from sqlalchemy.schema import CreateSchema
from prometheus_client import Counter, Histogram, generate_latest
from routes import fetch_article, document

from scripts import *
from database.chat import Base

# init_logger()

@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Purpose: Create Schema and tables if not exist
    """
    # Uncomment the below code for other database like postgresql
    # if DB_SCHEMA and DB_SCHEMA != 'public':
    #     async with engine.connect() as conn:
    #         await conn.execute(CreateSchema(DB_SCHEMA, if_not_exists=True))
    #         await conn.commit()
    #         print("Schema Creation Completed")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield   

app = FastAPI(
    title='Patient Data Management',
    description="The PDM application will help maintain patients' historical medication records and allow doctors to chat with an LLM model to gain insights about the drugs.",
    version= "1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

REQUEST_TIME = Histogram("rhttp_request_duration_seconds", "Duration of HTTP request in seconds", ["method", "endpoint", "status_code"])
REQUEST_COUNTER = Counter("http_request_total", "Total HTTP requests", ["method", "endpoint", "status_code"])
ERROR_COUNTER = Counter("http_errors_total", "Total number of error requests", ["method", "endpoint", "status_code"])

@app.middleware("http")
async def track_metrics(request:Request, call_next):
    try:
        method = request.method
        endpoint= request.url.path

        logging.info(f"request: {method} {request.url}")
        print(f"request: {method} {request.url}")

        start_time = time.time()

        response = await call_next(request)
        status_code = response.status_code

        duration = time.time() - start_time
        duration_ms = round(duration * 1000, 2)
        REQUEST_TIME.labels(method=method, endpoint=endpoint, status_code=status_code).observe(duration_ms)
        REQUEST_COUNTER.labels(method=method, endpoint=endpoint, status_code=status_code).inc()

        logging.info(f"Completed Request: {request.method} {request.url}")
        logging.error(f"Status: {response.status_code} Duration: {duration_ms} ms")
        return response
    except Exception:
        logging.error(f"Error Processing Request: {request.method} {request.url}")
        logging.error(f"Error Details: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"Detail": "Internal Server Error"})
        
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation Error: {exc.errors()}")
    logging.error(f"Request Body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())}
    )

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.get("/")
async def root():
    """
    Welcome message on the application startup
    """
    return {"Welcome to the AE&I applciation"}

@app.get("/get_status")
async def get_status():
    """
    Status of the Application
    """
    return JSONResponse({"status": "Status OK"})

# Include the routers
app.include_router(fetch_article.router, prefix='/article')
app.include_router(document.router, prefix='/document')



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)