import os
import discord
from myclient import MyClient

# 환경 변수 로드

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 클라이언트 객체 생성 및 실행
# 인텐트 및 클라이언트 객체 생성
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
