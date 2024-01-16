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
        #테스트 전용 코드
        elif message.content == '!add':
            discord_id = str(message.author.id)

            # 봇이 포인트 추가 금액을 물어봄
            await message.channel.send("얼마를 추가할까요?")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            try:
                amount_message = await self.wait_for('message', check=check, timeout=30.0)
                amount = int(amount_message.content)  # 여전히 숫자로 변환은 필요함

                # 포인트 추가 함수 호출
                add_success, new_points = add_points(self.connection, discord_id, amount)
                if add_success:
                    await message.channel.send(f"{amount}포인트가 추가되었습니다. 새로운 포인트: {new_points}")
                else:
                    await message.channel.send("포인트 추가에 실패했습니다.")
            except asyncio.TimeoutError:
                await message.channel.send('시간 초과입니다. 다시 시도해주세요.')
            except ValueError:
                await message.channel.send('잘못된 금액입니다. 숫자를 입력해주세요.')
        elif message.content == '!minus':
            discord_id = str(message.author.id)

            # 봇이 포인트 추가 금액을 물어봄
            await message.channel.send("얼마를 뺼까요?")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            try:
                amount_message = await self.wait_for('message', check=check, timeout=30.0)
                amount = int(amount_message.content)  # 여전히 숫자로 변환은 필요함

                # 포인트 추가 함수 호출
                minus_success, new_points = deduct_points(self.connection, discord_id, amount)
                if minus_success:
                    await message.channel.send(f"{amount}포인트가 추가되었습니다. 새로운 포인트: {new_points}")
                else:
                    await message.channel.send("포인트 추가에 실패했습니다.")
            except asyncio.TimeoutError:
                await message.channel.send('시간 초과입니다. 다시 시도해주세요.')
            except ValueError:
                await message.channel.send('잘못된 금액입니다. 숫자를 입력해주세요.')
        elif message.content == '!포인트':
            discord_id = str(message.author.id)

            # 사용자의 현재 포인트를 조회
            user_points = get_user_points(self.connection, discord_id)

            # 사용자에게 현재 포인트를 메시지로 전송
            await message.channel.send(f"현재 보유하신 포인트는 {user_points}포인트입니다.")

        else:
            answer = get_answer(message.content)
            if answer:
                await message.channel.send(answer)





