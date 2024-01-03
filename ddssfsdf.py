import discord
import os
from datetime import datetime
import random
#sex
# 환경 변수에서 토큰 가져오기 (보안 강화)
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_points = {}  # 유저 포인트를 저장할 딕셔너리

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '섹':
            await message.channel.send(f'스 {message.author.mention}')
        elif message.content.startswith('!game'):
            await self.play_game(message)
        elif message.content.startswith('!register'):
            await self.register_user(message)
        elif message.content.startswith('!points'):
            await self.show_points(message)
        else:
            answer = self.get_answer(message.content)
            if answer:
                await message.channel.send(answer)

    async def play_game(self, message):
        choices = ['가위', '바위', '보']
        bot_choice = random.choice(choices)
        await message.channel.send(f'봇이 선택한 것은 {bot_choice}입니다!')

    async def register_user(self, message):
        user_id = message.author.id
        if user_id not in self.user_points:
            self.user_points[user_id] = 100  # 초기 포인트
            await message.channel.send(f'{message.author.mention} 님이 등록되었습니다. 초기 포인트: 100')
        else:
            await message.channel.send(f'{message.author.mention} 님은 이미 등록되어 있습니다.')

    async def show_points(self, message):
        user_id = message.author.id
        if user_id in self.user_points:
            points = self.user_points[user_id]
            await message.channel.send(f'{message.author.mention} 님의 포인트: {points}')
        else:
            await message.channel.send(f'{message.author.mention} 님은 등록되지 않았습니다.')

    def get_day_of_week(self):
        weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
        weekday = weekday_list[datetime.today().weekday()]
        date = datetime.today().strftime("%Y년 %m월 %d일")
        return f'{date}({weekday})'

    def get_time(self):
        return datetime.today().strftime("%H시 %M분 %S초")

    def get_answer(self, text):
        trim_text = text.replace(" ", "")
        answer_dict = {
            '안녕': '안녕하세요. 키타 이쿠요입니다.',
            '요일': f':calendar: 오늘은 {self.get_day_of_week()}입니다',
            '시간': f':clock9: 현재 시간은 {self.get_time()}입니다.',
        }

        if not trim_text:
            return None
        return answer_dict.get(trim_text, None)

# 인텐트 및 클라이언트 객체 생성
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
