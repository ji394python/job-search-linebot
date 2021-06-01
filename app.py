import os
from datetime import datetime

from flask import Flask, abort, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent,MessageEvent, TextMessage, TextSendMessage
from random import randint
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from json import load 

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello GCP"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)  #官方拿來驗證linePlatform的訊息是否真的為linePlatform發來
        except InvalidSignatureError:
            abort(400)

        return "OK"

##監聽程序，前面要處理的事件類別，後面放要用甚麼格式來回復訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    get_userId = event.source
    if get_message == "職缺":
        df = pd.read_csv('data/工程師_work.csv')
        random = randint(0,len(df))
        row = df.iloc[random,]
        reply = TextSendMessage(text=f" [抽獎] \n 職缺：{row['職缺']} \n 公司：{row['職缺公司']} \n 地點：{row['工作地點']} \n 薪水：{row['薪水']}")
    line_bot_api.reply_message(event.reply_token, reply)
    line_bot_api.push_message('U59c9b989be10bed54b972766530b9fb9', TextSendMessage(text=f"{get_userId} \n {get_message}"))

@handler.add(FollowEvent)
def handle_message(event):
    # Send To Line
    reply = TextSendMessage(text=f"[感謝您加我為好友QQ]")
    line_bot_api.reply_message(event.reply_token, reply)