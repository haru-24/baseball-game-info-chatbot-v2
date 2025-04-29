from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    message: str = Field(description="ユーザーメッセージ")


class AIResponse(BaseModel):
    message: str = Field(description="AIからの応答メッセージ")
