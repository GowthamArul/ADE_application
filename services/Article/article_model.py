from pydantic import BaseModel, ConfigDict

class ArxivArticleRequest(BaseModel):
    search_query : str
    start : int
    max_results: int 
    model_config = {
        "json_schema_extra": {
            "examples": [
            {
        'search_query': "Cancer",
        'start': 0,
        'max_results': 10,
            } ]
                            }
    }

class ArxivArticle(BaseModel):
    id: str
    title: str
    authors: str
    summary: str
    primary_category: str
    secondary_categories: str | None
    publication_date: str
    updated_date: str
    link: str

    model_config = ConfigDict(from_attributes=True)


class ArxivFetchResponse(BaseModel):
    articles: list[ArxivArticle]
    count: int


