import discord
from utils import *
from commands import *
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '섹':
            await message.channel.send(f'스 {message.author.mention}')
        elif message.content.startswith('!game'):
            await play_game(message)
        elif message.content.startswith('!register'):
            await register_user(self, message)
        elif message.content == '!전체경기':
            await show_all_matches(message)
        elif message.content == '!경기':
            await show_current_week_matches(message)
        elif message.content == '!베팅':
            await get_betting_predictions(self, message)
        else:
            answer = get_answer(message.content)
            if answer:
                await message.channel.send(answer)





