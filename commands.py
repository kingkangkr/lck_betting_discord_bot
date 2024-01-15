import random
from utils import *
from match_data import matches
from get_odds_of_matches import odds_list
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
        # 해당 경기의 배당률 정보 가져오기
        odds = odds_list[i] if i < len(odds_list) else (None, None)

        # 팀 선택 프롬프트
        team_prompt = f"{match[0]} vs {match[1]} - {match[0]} 배당: {odds[0]}, {match[1]} 배당: {odds[1]}. 승리 팀을 선택해주세요 (1 또는 2): "
        await message.channel.send(team_prompt)

        def check_team_choice(m):
            return m.author == message.author and m.channel == message.channel and m.content in ['1', '2']

        try:
            team_choice = await client.wait_for('message', check=check_team_choice, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('시간 초과입니다. 다시 시도해주세요.')
            return

        # 베팅 금액 프롬프트
        bet_amount_prompt = f"얼마를 베팅하시겠습니까? 금액을 입력해주세요: "
        await message.channel.send(bet_amount_prompt)

        def check_bet_amount(m):
            return m.author == message.author and m.channel == message.channel and m.content.isdigit()

        try:
            bet_amount = await client.wait_for('message', check=check_bet_amount, timeout=30.0)
        except asyncio.TimeoutError:
            await message.channel.send('시간초과입니다.다시시도해주세요.')
            return
        selected_team = int(team_choice.content) - 1  # 선택한 팀 인덱스
        bet_amount_value = int(bet_amount.content)
        potential_earnings = int(bet_amount_value * odds[selected_team]) if odds[selected_team] else 0
        betting_predictions.append((team_choice.content, bet_amount.content, potential_earnings))

        # 모든 베팅 정보와 예상 수익 출력
    for i, prediction in enumerate(betting_predictions):
        selected_team_index = int(prediction[0]) - 1  # 선택한 팀 인덱스 (0 또는 1)
        team_name = week_matches[i][selected_team_index]  # 선택한 팀 이름
        await message.channel.send(f"선택한 팀: {team_name} ({prediction[0]}), 베팅 금액: {prediction[1]}, 맞히면 얻는 금액: {prediction[2]}")


