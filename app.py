#載入LineBot所需要的套件
from ast import Store
from curses.ascii import isdigit
import profile
import re
from secrets import choice
from telnetlib import IP
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
app = Flask(__name__)

import random
import MongoDB_Game1
import MongoDB_profile
import Coody_reply_msg

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('Orj4xNTzu4lZEwnUuf5B1Sdez01KSPtyBo1UC1ZnpPS93AMguOYc4XkQuw1BqIIDdmgITw4guIGtkJJ98w/y3sUM3MqXFQoaXtpw4bzWVuB0fxdCa3a2sGzRVS2W+HqOJOHV8BIGzl3QQe3ygcw4hAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('551d866b1602853292a0c02b7ef8055c')

line_bot_api.push_message('Ua228ca9743237fb1fb497b4b3d0247c9', TextSendMessage(text='啊～抱歉！不小心睡著了'))
ID='Ua228ca9743237fb1fb497b4b3d0247c9'
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def is_number(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
def is_string(string):
    return isinstance(string,str)
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg =event.message.text
    user_id = event.source.user_id
    reply_message="品澤寫錯嘍"
    if MongoDB_profile.check_profil_exist(user_id):#確認是否有使用者資料
        IP_profile=MongoDB_profile.find_profile(user_id)
    else:
        Profile={"User_Id":user_id,"Status":"Standard"}
        MongoDB_profile.store_profile(Profile)
    
    if re.match("寶寶遊戲",msg):#遊戲選項
        MongoDB_profile.update_Status(user_id,"Game_Rule")
        flex_message=TextSendMessage(
            text="玩什麼遊戲呢？",
            quick_reply=QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="數字炸彈",text="放馬過來～")),
            QuickReplyButton(action=MessageAction(label="猜猜英文",text="Go~Go~"))
            ]))
        line_bot_api.reply_message(event.reply_token,flex_message)
    

    if IP_profile["Status"]=="Game_Rule":#遊戲規則
        if re.match("放馬過來",msg):
            MongoDB_profile.update_Status(user_id,"Game_1Rule")
            flex_message=TextSendMessage(
                text="我會隨機出一個數字\n(最小為0 最大為你指定的最大數字上限)\n讓你猜💣",
                quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="開始吧",text="Bump!!!")),
                QuickReplyButton(action=MessageAction(label="放棄了～",text="不玩啊"))
            ]))
            line_bot_api.reply_message(event.reply_token,flex_message)
        elif re.match("Go~Go~",msg):
            MongoDB_profile.update_Status(user_id,"Game_2Rule")
            flex_message=TextSendMessage(
                text="我會隨機出一個數字\n(最小為0 最大為你指定的最大數字上限)\n讓你猜💣",
                quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="開始吧",text="Let's go~")),
                QuickReplyButton(action=MessageAction(label="放棄了～",text="不玩啦"))
            ]))
            line_bot_api.reply_message(event.reply_token,flex_message)
    elif IP_profile["Status"]=="Game_Rule" and re.match("不玩啦",msg):
        MongoDB_profile.update_Status(user_id,"Standard")
        reply_message="可惡!怎麼能說不完就不玩😡"


    if re.match("Bump!!!",msg) and IP_profile["Status"]=="Game_1Rule":#Game_1      
        MongoDB_profile.update_Status(user_id,"Game1_Ready")
        reply_message="請輸入你要跟我玩奪大～"
    elif is_number(msg) and IP_profile["Status"]=="Game1_Ready":
        MongoDB_Game1.Initial_Game1(user_id,msg)
        MongoDB_profile.update_Status(user_id,"Game1_Playing")
        reply_message="請媽媽輸入你猜的數字(最小為1):"
    elif is_number(msg) and IP_profile["Status"]=="Game1_Playing":
        reply_message=MongoDB_Game1.play_game(user_id,msg)

    if re.match("Let's go~",msg) and IP_profile["Status"]=="game_2Rule":
        MongoDB_profile.update_Status(user_id,"Game2_Ready")




    if re.match("酷弟",msg):#回復酷弟訊息
        choice_string=Coody_reply_msg.Coody_message()
        choice_sticker=random.choice([52114120,52114116,52114129,52114125,52114114,52114112,52114122,52114147,52114115])#酷地回覆sticker,查詢網址：https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
        sticker_message = StickerSendMessage(
        package_id='11539',
        sticker_id=choice_sticker )

        rand=random.randint(1,2)#隨機傳送貼圖或者訊息
        if rand==1:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(choice_string))
        elif rand==2:
            line_bot_api.reply_message(event.reply_token,sticker_message)

    if re.match("學習打招呼",msg):#學習打招呼 Coody_reply_msg
        MongoDB_profile.update_Status(user_id,"Learning_New_Greet")
        reply_message="請輸入想讓寶寶學習什麼！！"
    elif is_string(msg) and IP_profile["Status"]=="Learning_New_Greet":
        reply_message=Coody_reply_msg.learning_Greet(msg)
        MongoDB_profile.update_Status(user_id,"Standard")


    line_bot_api.reply_message(event.reply_token,TextSendMessage(reply_message))


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)