import discord
import json
import re
from lib.bodoge_bot import dice


# discord client
client = discord.Client()

# ダイス用
dice_pattern = re.compile('^\d+d\d+$', re.IGNORECASE)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message: discord.message.Message):
    # <Message id=850997242483048449 channel=<TextChannel id=850956584506621987 name='一般' position=0 nsfw=False news=False category_id=850956584506621985> type=<MessageType.default: 0> author=<Member id=361013825685684224 name='yn,dispyaaaaaaaaaaaaaaaaaaaaaaaa' discriminator='1552' bot=False nick=None guild=<Guild id=850956584506621984 name='bodoge_bot_test' shard_id=None chunked=False member_count=2>> flags=<MessageFlags value=0>>

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # channelに投稿される
    await message.channel.send(f'you said {message.content}. channel')
    # DMになる
    # await message.author.send(f'you said {message.content}. author')

    # dice
    if dice_pattern.match(message.content) is not None:
        dice_sum, dice_history, dice_histgram = dice(message.content)
        await message.channel.send(f'sum:{dice_sum} \nhistory:{dice_history}\nhistgram:{dice_histgram}')
        return



    # if message.content == '/regist':
    #      await message.channel.send('call regist @channel')
    #      await message.author.send('call regist @author')


# 接続に必要なオブジェクトを生成
with open('.env.json') as f:
    bot_key = json.load(f)

client.run(bot_key['TOKEN'])

