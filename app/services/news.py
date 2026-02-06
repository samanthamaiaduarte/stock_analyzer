import requests
import json

from app.core.settings import settings

class News:

    def __init__(self, ticker: str, time_period: str = "last_month", engine: str = "google"):
        self.ticker = ticker
        self.time_period = time_period
        self.engine = engine
        self.url = "https://www.searchapi.io/api/v1/search"

    def __get_x_opinions(self) -> list:
        params = {
        "engine": self.engine,
        "q": f"x opinions about {self.ticker} ticker",
        "api_key": settings.SEARCH_API_KEY,
        "time_period": self.time_period
        }

        response_x = requests.get(self.url, params=params)
        return json.loads(response_x.text).get("organic_results", [])
    
    def __get_organic_news(self) -> list:
        params = {
        "engine": self.engine,
        "q": f"news that impact {self.ticker} ticker",
        "api_key": settings.SEARCH_API_KEY,
        "time_period": self.time_period
        }

        response_news = requests.get(self.url, params=params)
        return json.loads(response_news.text).get("organic_results", [])
    
    def get_report(self) -> str:
        organic_x_results = self.__get_x_opinions()
        organic_news_results = self.__get_organic_news()

        STOCK_NEWS = f"Recent News and Opinions about {self.ticker}:"
        for result in organic_x_results:
            STOCK_NEWS += f"""
            Position: {result.get('position', 'N/A')}
            Link: {result.get('link', 'No opinions found')}
            Source: {result.get('source', '')}
            Snippet: {result.get('snippet', '')}
            """
        for result in organic_news_results:
            STOCK_NEWS += f"""
            Position: {result.get('position', 'N/A')}
            Link: {result.get('link', 'No news found')}
            Source: {result.get('source', '')}
            Snippet: {result.get('snippet', '')}
            """

        return STOCK_NEWS