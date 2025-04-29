from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.models import models
from app.prompts.prompt import DEFULT_PROMPT
from app.services.baseball_scrayper import BaseballScraper

load_dotenv()


class GPTService:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        self._llm = ChatOpenAI(model=model, temperature=temperature)
        self._messages = [
            SystemMessage(content=DEFULT_PROMPT),
        ]

    def talk(self, user_message: models.UserMessage) -> models.AIResponse:
        """
        GPT-4o-Miniと会話するメソッド
        """
        bs_scraper = BaseballScraper()
        self._messages.append(SystemMessage(content=bs_scraper.get_today_games()))
        self._messages.append(HumanMessage(content=user_message.message))
        ai_response = self._llm.invoke(self._messages)
        if not ai_response.content:
            raise HTTPException(status_code=500, detail="AI response is empty")
        self._messages.append(AIMessage(content=ai_response.content))
        return models.AIResponse(message=ai_response.content)
