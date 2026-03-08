from fastapi import APIRouter, Request, HTTPException, Depends
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from sqlalchemy.orm import Session
from datetime import datetime
import os
import database
import models

router = APIRouter(tags=["Line Webhook"])

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
channel_secret = os.getenv("LINE_CHANNEL_SECRET", "")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@router.post("/webhook/line")
async def line_webhook(request: Request, db: Session = Depends(database.get_db)):
    signature = request.headers.get("X-Line-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="X-Line-Signature header is missing")

    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        # 將 db 放入 handler 執行環境的方法：
        # handler 本身不支持 dependency injection，我們可以在這裡自行解析 events，
        # 或者把 db 設為全域範圍（不推薦）。
        # 最好的方式是手動呼叫 parser。
        
        from linebot import WebhookParser
        parser = WebhookParser(channel_secret)
        events = parser.parse(body_str, signature)
        
        for event in events:
            if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
                handle_text_message(event, db)
                
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

def handle_text_message(event: MessageEvent, db: Session):
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    # 檢查是否為 6 位數 OTP 格式
    if len(text) == 6 and text.isdigit():
        # 在資料庫尋找未過期的 OTP
        user = db.query(models.User).filter(
            models.User.line_otp == text,
            models.User.line_otp_expires_at > datetime.utcnow()
        ).first()

        if user:
            # 綁定成功
            user.line_token = user_id
            user.line_otp = None
            user.line_otp_expires_at = None
            db.commit()
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="綁定成功！您現在會收到價格通知了。")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="驗證碼無效或已過期，請在網頁端重新產生！")
            )
    else:
        # 如果使用者傳送其他訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入網頁端顯示的 6 位數綁定驗證碼。")
        )
