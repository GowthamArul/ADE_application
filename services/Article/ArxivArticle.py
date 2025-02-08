import logging
import requests
from .article_model import ArxivArticle
import xml.etree.ElementTree as ET
import re

class ArxivArticleScrape:
    def __init__(self, API_KEY=None):
        self.api_key = API_KEY
        self.base_url = "http://export.arxiv.org/api/query?"
    
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
            extract_tag = '{http://www.w3.org/2005/Atom}'
            
            for entry in xml_string.findall(f'{extract_tag}entry'):
                # Store the values in a dictionary
                articles.append({
                    'title': entry.find(f'{extract_tag}title').text,
                    'authors': ', '.join([author.find(f'{extract_tag}name').text for author in entry.findall(f'{extract_tag}author')]),
                    'summary': (entry.find(f'{extract_tag}summary').text).replace("\n", " "),
                    'link': entry.find(f'{extract_tag}link').attrib['href'],
                    'publication_date': re.sub(r'[A-Za-z]', ' ', entry.find(f'{extract_tag}published').text),
                    'updated_date': re.sub(r'[A-Za-z]', ' ', entry.find(f'{extract_tag}updated').text)
                })
                print( entry.find(f'{extract_tag}title').text)
            
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

    def scrape(self, payload:ArxivArticle):
        try:
            print("The search query is ",payload.search_query)
            articles = self._search_arxiv(payload.search_query
                                    )
            print('The Article is : ',articles)
            articles_dict = self._parse_article_xml(articles)
            return articles_dict
        except Exception as ex:
            print(f'Error in fetching article {ex}')