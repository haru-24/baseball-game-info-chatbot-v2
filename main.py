import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage
from pydantic import BaseModel, Field

app = FastAPI()
load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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


@app.post("/talk", response_model=AIResponse)
def ai_talk(user_message: UserMessage) -> AIResponse:
    try:
        ai_message = user_message.message
        return AIResponse(message=ai_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
