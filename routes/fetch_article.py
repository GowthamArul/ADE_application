import logging

from fastapi import APIRouter, Request
from services.Article.article_model import ArxivArticle, ArxivFetchResponse, ArxivArticleRequest
from services.Article.ArxivArticle import ArxivArticleScrape


router = APIRouter()

@router.post("/fetchatricle", tags=["Fetch Arxiv Articles"])
async def fetch_articles(request:ArxivArticleRequest) -> ArxivFetchResponse:
    try:
        article_obj = ArxivArticleScrape()
        response = article_obj.scrape(request)
        return response
    except Exception as ex:
        print(f"Error in extracting Articles {ex}")