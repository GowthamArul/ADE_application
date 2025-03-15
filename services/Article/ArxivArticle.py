import logging
import requests
from services.Article.article_model import *
import xml.etree.ElementTree as ET
import re
import traceback
import json


class ArxivArticleScrape:
    def __init__(self, API_KEY=None):
        self.api_key = API_KEY
        self.base_url = "http://export.arxiv.org/api/query?"
        self.category = self.load_cat_json()

    def load_cat_json(self):
        with open('configs/category.json', "r") as f:
            cat_data = json.load(f)
            return cat_data
    
    def _cat_lookup(self,cat_code:list) -> str:
        ls = []
        for i in cat_code:
            if i in self.category.keys():
                ls.append(self.category[i])
        if len(ls) > 1:
            return ", ".join(ls)
        else:
            return "".join(ls)

    
    def _parse_article_xml(self, xml_string):
        try:
            """
            Parses a Article XML string containing multiple articles.
            Args:
                xml_string (BeautifulSoup): The XML string containing multiple articles.
            Returns:
                List[Dict[str, Any]]: A list of dict, each representing a parsed article.
            
            """
            articles = []
            ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in xml_string.findall('atom:entry', ns):
                # Store the values in a dictionary
                article_id = entry.find('atom:id', ns).text.strip().split("/")[-1]
                title = (entry.find('atom:title', ns).text).replace("\n", "").strip()
                authors = (', '.join([author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)])).replace("\n", "").strip()
                summary = (entry.find('atom:summary', ns).text).replace("\n", "").strip()
                link = entry.find('atom:link', ns).attrib['href']
                publication_date = (entry.find('atom:published', ns).text)
                updated = (re.sub(r'[A-Za-z]', ' ', entry.find('atom:updated', ns).text)).replace("\n", "").strip()
                primary_category = [(entry.find('arxiv:primary_category', ns).attrib['term']).replace("\n", "").strip()]
                
                # Extract all categories
                categories = [cat.attrib['term'] for cat in entry.findall('atom:category', ns)]
                cat = [i for i in categories if i not in primary_category]
                # Store the values in a dictionary
                article_info = {
                    'id': article_id,
                    'title': title,
                    'authors': authors,
                    'summary': summary,
                    'link': link,
                    'publication_date': publication_date,
                    'updated_date': updated,
                    'primary_category': self._cat_lookup(primary_category),
                    'secondary_categories': self._cat_lookup(cat) if self._cat_lookup(cat) != "" else None
                }
                
                # Add the dictionary to the list of articles
                articles.append(article_info)
            
            return articles
        except Exception as ex:
            print(f"Error in Article XML {ex}")

    def _search_arxiv(self, query, max_results=5, start=0):
        try:
            params = {
                'search_query': query,
                'start': start,
                'max_results': max_results,
            }
            # Get the raw XML response
            result = requests.get(self.base_url, params=params)
            
            # Parse the XML response using ElementTree
            response = ET.fromstring(result.text)
            return response
        except Exception as ex:
            print(f"Error in Extracting Articles {ex}")

    def scrape(self, payload:ArxivArticleRequest):
        try:
            articles = self._search_arxiv(payload.search_query, 
                                          payload.max_results, 
                                          payload.start
                                        )
            articles_dict = self._parse_article_xml(articles)
            print(articles_dict)
            return ArxivFetchResponse(articles=articles_dict, count=len(articles_dict))
        except Exception as ex:
            print(traceback.format_exc)
            print(f'Error in fetching article {ex}')
