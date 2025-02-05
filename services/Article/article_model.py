from pydantic import BaseModel

class ArxivArticle(BaseModel):
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
    
class ArxivArticleResponse(BaseModel):
    title: str
    authors: str
    summary: str
    link: str