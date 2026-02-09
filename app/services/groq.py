from langchain_groq import ChatGroq
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage

from app.core.settings import settings

from app.ai.prompts.human_prompt import HUMAN_PROMPT
from app.ai.prompts.system_prompt import SYSTEM_PROMPT
from app.ai.structured_output.ai_response import AIResponse

from app.services.finance import Finance
from app.services.news import News

class GroqModel:

    def __init__(self, model_name: str = "llama-3.3-70b-versatile", temperature : float = 0.1):
        self.model = ChatGroq(model=model_name, temperature=temperature, api_key=settings.GROQ_API_KEY).with_structured_output(AIResponse)

    def __get_message(self, ticker: str) -> list[AnyMessage]:
        finance = Finance(ticker)
        news = News(ticker)
    
        stock_statistics = finance.get_report()
        stock_news = news.get_report()

        return [
            SystemMessage(content=SYSTEM_PROMPT.replace("{TICKER}", ticker)),
            HumanMessage(content=HUMAN_PROMPT.replace("{STOCK_STATISTICS}", stock_statistics).replace("{STOCK_NEWS}", stock_news))
        ]
    
    def get_response(self, ticker: str) -> AIResponse:
        return self.model.invoke(self.__get_message(ticker))