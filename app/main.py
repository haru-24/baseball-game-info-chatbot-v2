import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage

from app.models import models
from app.services.gpt_service import GPTService

load_dotenv()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature=Header(None),
):
    body = await request.body()
    try:
        background_tasks.add_task(handler.handle, body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "ok"


@handler.add(MessageEvent)
def handle_message(event: MessageEvent):
    if event.type != "message" or event.message.type != "text":
        return

    gpt_service = GPTService()
    ai_message = gpt_service.talk(models.UserMessage(message=event.message.text))
    if not ai_message:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="エラーが発生しました"))
        return
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_message.message))


@app.post("/talk", response_model=models.AIResponse)
def ai_talk(user_message: models.UserMessage) -> models.AIResponse:
    try:
        gpt_service = GPTService()
        gpt_service.talk(user_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
