import discord
from commands import *
from texts import video_links

manager_discord_id = 336394598781943809


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '섹':
            await message.channel.send(f'스 {message.author.mention}')

        elif message.content.startswith('!game'):
            await play_game(message)

        elif message.content.startswith('!register') or message.content == '!등록' or message.content == '!ㄷㄹ':
            await register_user(self, message)

        elif message.content == '!전체경기' or message.content == '!ㅈㅊㄱㄱ':
            await show_all_matches(message)

        elif message.content == '!경기' or message.content == '!ㄱㄱ':
            await show_current_week_matches(message)

        elif message.content == '!베팅' or message.content == '!ㅂㅌ':
            await get_betting_predictions(self, message)

        elif message.content == '!포인트' or message.content == '!ㅍㅇㅌ':
            discord_id = str(message.author.id)
            # 사용자의 현재 포인트를 조회
            user_points = get_user_points(self.connection, discord_id)
            # 사용자에게 현재 포인트를 메시지로 전송
            await message.channel.send(f"현재 보유하신 포인트는 {user_points}포인트입니다.")

        elif message.content in ["!출석체크", "!ㅊㅊ", '!cc']:
            discord_id = str(message.author.id)
            await attendance_check(self.connection, discord_id, message)

        elif message.content == "!순위" or message.content == "!ㅅㅇ":
            await show_rank(message)

        elif message.content == "!주간결산" and message.author.id == manager_discord_id:
            await handle_weekly_summary(message, self.connection, odds_list)

        elif message.content == "!하이라이트" or message.content == "!ㅎㅇㄹㅇㅌ":
            response = "방장 추천 LCK 영상:\n"
            for week, link in video_links.items():
                response += f"{week}: {link}\n"
            await message.channel.send(response)

        elif message.content == "!블랙잭" or message.content == "!ㅂㄹㅈ":
            await start_blackjack_game(self, message)

        elif message.content == "!명령어" or message.content == '!ㅁㄹㅇ':
            await message.channel.send(commands_info)
        # elif message.content.startswith('!문제'):
        #     await self.math_quiz(message)

        elif message.content == "!공지":
            await message.channel.send(announcement)

        else:
            answer = get_answer(message.content)
            if answer:
                await message.channel.send(answer)
