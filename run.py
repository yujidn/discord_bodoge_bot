import sys
import discord
import json
import re
import cv2
import os
import random
from lib.bodoge_bot import dice
from lib.flask_server import flask_run, GET_IMAGE_NAME
from lib.image_source_server import image_server_run
from lib.image_process import image_rotate_ccw, image_divide
import threading

MAX_PLAYER = 6
PLAYER_VIEW_PREFIX = "pv_"
FIELD_COL = 3
FIELD_ROW = 2

bot_commands = {
    "help": ["/help", "/h"],
    "init": ["/init"],
    "image_update": ["/image_update", "/iu"],
    "regist": ["/regist", "/r"],
    # "onymous_chat": ["/onymous", "/o"],
    # "anomymous_chat": ["/anonymous", "/a"],
    "open_onymous_chat": ["/onymous_chat", "/oc"],
    "open_anonymous_chat": ["/anonymous_chat", "/ac"],
    "shutdown": ["/shutdown"],
}

# discord client
client = discord.Client()

# コマンド判定用パターンマッチ
dice_pattern = re.compile("^\d+d\d+$", re.IGNORECASE)
r1 = "\\" + bot_commands["regist"][0]
r2 = "\\" + bot_commands["regist"][1]
regist_pattern = re.compile(f"^{r1}|^{r2} \d$")

# 画像受信サーバー
flask_thread = threading.Thread(target=flask_run)
image_server_thread = threading.Thread(target=image_server_run)
flask_thread.setDaemon(True)
image_server_thread.setDaemon(True)
flask_thread.start()
image_server_thread.start()

# 状態初期化処理
player_list = [None] * (MAX_PLAYER + 1)
last_message = {}


def init():
    global player_list
    global last_message
    player_list = [None] * (MAX_PLAYER + 1)
    last_message = {}


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")


# メッセージ受信時に動作する処理
# botへのDMもこのイベントが活性する
@client.event
async def on_message(message: discord.message.Message):

    # channelに投稿される
    # 物のメッセージがdmだった場合は、このコマンドでDMになる
    # await message.channel.send(f"you said {message.content}. channel")
    # DMになる
    # await message.author.send(f'you said {message.content}. author')

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # botへのDMの場合
    if message.guild is None:
        # dmの場合はmessage.channel.sendで返送すると、DMでの返送になる
        player_name = message.author.name
        last_message[player_name] = message.content
        await message.channel.send(f"最後のメッセージを {message.content} に更新しました")
        return

    # channnelへの投稿だった場合
    else:
        # dice
        if dice_pattern.match(message.content) is not None:
            dice_sum, dice_history, dice_histgram = dice(message.content)
            await message.channel.send(
                f"sum:{dice_sum} \nhistory:{dice_history}\nhistgram:{dice_histgram}"
            )
            return

        # init
        if message.content in bot_commands["init"]:
            init()
            await message.channel.send("初期化しました")
            return

        # regist
        if regist_pattern.match(message.content) is not None:
            sp = message.content.split(" ")
            player_number = int(sp[1])
            player_name = message.author.name

            if player_number < 1:
                await message.channel.send("player_numberは1以上の値にしてください")
                return

            if player_number > MAX_PLAYER:
                await message.channel.send(f"player_numberは{MAX_PLAYER}以下の値にしてください")
                return

            player_list[player_number] = {
                "player_number": player_number,
                "player_name": player_name,
                "last_chat": "",
                "message": message,
            }

            await message.channel.send(
                f"{player_name} を player_number:{player_number} に登録しました"
            )
            return

        # open chat
        if message.content in bot_commands["open_onymous_chat"]:
            m = ""
            for k, v in last_message.items():
                m += f"{k} : {v}\n"
            await message.channel.send(m)
            return

        if message.content in bot_commands["open_anonymous_chat"]:
            vs = []
            for v in last_message.values():
                vs.append(v)

            random.shuffle(vs)
            m = ""
            for v in vs:
                m += f"{v}\n"
            await message.channel.send(m)
            return

        # 画像を送信したりする
        if message.content in bot_commands["image_update"]:
            image = cv2.imread(GET_IMAGE_NAME)
            image = image_rotate_ccw(image)
            image_divide(image, FIELD_COL, FIELD_ROW)

            for pl in player_list:
                if pl is None:
                    continue

                number = pl["player_number"]
                dm = pl["message"].author
                filepath = f"{PLAYER_VIEW_PREFIX}{number}.jpg"
                if os.path.exists(filepath):
                    df = discord.File(filepath, filename=filepath)
                    await dm.send(file=df)
                else:
                    await message.channel.send(f"file not exist. {filepath}")
            return

        # botの終了
        if message.content in bot_commands["shutdown"]:
            await message.channel.send("good bye")
            sys.exit()


# 接続に必要なオブジェクトを生成
with open(".env.json") as f:
    bot_key = json.load(f)

client.run(bot_key["TOKEN"])
