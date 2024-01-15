import random
from utils import *
from match_data import matches
from get_odds_of_matches import formatted_matches
import asyncio

async def play_game(message):
    choices = ['가위', '바위', '보']
    bot_choice = random.choice(choices)
    await message.channel.send(f'봇이 선택한 것은 {bot_choice}입니다!')
# ㅎㅇ
async def register_user(client,message):
    discord_id = str(message.author.id)  # Get the Discord ID of the user
    name = message.author.name           # Get the Discord Name of the user

    # Check if the user is already registered
    if is_user_registered(client.connection, discord_id):
        await message.channel.send("이미 등록되어 있습니다.")
    else:
        # Register the user with both discord_id and name
        register_new_user(discord_id, name)
        await message.channel.send(f"{message.author.mention}, 등록이 완료되었습니다.")

async def show_all_matches(message):
    response = "전체 경기 일정:\n" + format_matches_by_week(matches)
    await message.channel.send(response)

async def show_current_week_matches(message):
    week = get_current_week()
    if week is None:
        response = "현재 진행 중인 경기가 없습니다."
    else:
        matches_this_week = get_matches_for_current_week(week, matches)
        response = f"현재 주차: {week}주차 경기:\n"
        for match in matches_this_week:
            response += f"{match[0]} vs {match[1]}\n"
    await message.channel.send(response)
async def get_betting_predictions(client, message):
    current_week = get_current_week()
    if current_week is None:
        await message.channel.send("현재 진행 중인 경기가 없습니다.")
        return

    week_matches = get_matches_for_current_week(current_week, matches)
    betting_predictions = []

    for i, match in enumerate(week_matches):
        # formatted_matches에서 배당률 정보를 가져옴
        if i < len(formatted_matches):
            odds_info = formatted_matches[i]
        else:
            odds_info = f"{match[0]} vs {match[1]}"

        prompt = f"{odds_info} - {match[0]}의 승리는 1, {match[1]}의 승리는 2를 입력해주세요: "
        await message.channel.send(prompt)

        def check(m):
            return m.author == message.author and m.channel == message.channel and m.content in ['1', '2']

        try:
            response = await client.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('시간 초과입니다. 다시 시도해주세요.')
            return

        betting_predictions.append(response.content)

    await message.channel.send(f"당신의 베팅 결과: {''.join(betting_predictions)}")


