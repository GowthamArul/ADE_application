import logging

from fastapi import APIRouter, Request
from services.Article.article_model import ArxivArticle, ArxivArticleResponse
from services.Article.ArxivArticle import ArxivArticleScrape


router = APIRouter()

@router.post("/fetchatricle", tags=["Fetch Arxiv Articles"])
async def fetch_articles(request:ArxivArticle) -> list[ArxivArticleResponse]:
    try:
        article_obj = ArxivArticleScrape()
        print(request)
        response = article_obj.scrape(request)
        return response
    except Exception as ex:
        print(f"Error in extracting Articles {ex}")