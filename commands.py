import random
from utils import *
from match_data import matches
async def play_game(message):
    choices = ['가위', '바위', '보']
    bot_choice = random.choice(choices)
    await message.channel.send(f'봇이 선택한 것은 {bot_choice}입니다!')

async def register_user(message):
    discord_id = str(message.author.id)  # Get the Discord ID of the user
    name = message.author.name           # Get the Discord Name of the user

    # Check if the user is already registered
    if is_user_registered(discord_id):
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

