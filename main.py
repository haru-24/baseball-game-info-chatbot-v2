import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@app.get("/")
def read_root():
    return {"Hello": "Worl"}


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


class UserMessage(BaseModel):
    message: str = Field(description="メッセージ")


class AIResponse(BaseModel):
    message: str = Field(description="AIからの応答メッセージ")


@app.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature=Header(None),
):
    body = await request.body()
    try:
        background_tasks.add_task(
            handler.handle, body.decode("utf-8"), x_line_signature
        )
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "ok"


@handler.add(MessageEvent)
def handle_message(event: MessageEvent):
    if event.type != "message" or event.message.type != "text":
        return

    print(UserMessage(message=event.message.text))
    ai_message = ai_talk(UserMessage(message=event.message.text))
    if not ai_message:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="エラーが発生しました")
        )
        return
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=ai_message.message)
    )


messages = [
    SystemMessage(
        content="あなたの名前はパグ蔵です。あなたは犬です。語尾にガウをつけて話します。"
    ),
]


@app.post("/talk", response_model=AIResponse)
def ai_talk(user_message: UserMessage) -> AIResponse:
    try:
        messages.append(HumanMessage(content=user_message.message))
        ai_response = llm.invoke(messages)
        if not ai_response.content:
            raise HTTPException(status_code=500, detail="AI response is empty")
        messages.append(AIMessage(content=ai_response.content))
        return AIResponse(message=ai_response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
