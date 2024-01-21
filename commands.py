import random
import asyncio
from utils import *
from texts import *
from get_odds_of_matches import odds_list
from blackjack import BlackjackGame
#from math_question import generate_math_question

weekly_summaries = []
async def play_game(message):
    choices = ['가위', '바위', '보']
    bot_choice = random.choice(choices)
    await message.channel.send(f'봇이 선택한 것은 {bot_choice}입니다!')


async def register_user(client, message):
    discord_id = str(message.author.id)  # Get the Discord ID of the user
    name = message.author.name  # Get the Discord Name of the user

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
    current_week = get_bet_week_number(bet_date_ranges)
    if current_week is None:
        await message.channel.send("현재 진행 중인 경기가 없습니다.")
        return
    discord_id = str(message.author.id)  # 사용자의 Discord ID
    # Check if the user is registered
    if not is_user_registered(client.connection, discord_id):
        await message.channel.send("먼저 !register를 이용해서 사용자 등록을 해주세요.")
        return
    # 데이터베이스에서 동일한 주차와 Discord ID에 대한 베팅 확인
    cursor = client.connection.cursor()
    query = "SELECT * FROM Bets WHERE DiscordID = %s AND Week = %s"
    cursor.execute(query, (discord_id, current_week))
    existing_bet = cursor.fetchone()
    cursor.fetchall()
    cursor.close()

    if existing_bet:
        await message.channel.send("이미 이번 주에 베팅을 하셨습니다.")
        return
    cursor = client.connection.cursor()
    cursor.execute("SELECT Points FROM Users WHERE DiscordID = %s", (discord_id,))
    result = cursor.fetchone()
    if result is None:
        # No user record found in the database
        await message.channel.send("등록이 완료되지 않았습니다.")
        return
    else:
        user_points = result
    week_matches = get_matches_for_current_week(current_week, matches)
    betting_predictions = []
    all_saved_successfully = True  # 모든 저장이 성공했는지 추적하는 변수
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

        # 사용자의 현재 포인트 가져오기
        user_points = get_user_points(client.connection, discord_id)

        # 베팅 금액 프롬프트
        bet_amount_prompt = f"얼마를 베팅하시겠습니까? 현재 보유 포인트: {user_points}포인트. 베팅 금액으로 1을 입력할 시 기본 금액인 1000이 베팅 됩니다. 금액을 입력해주세요: "
        await message.channel.send(bet_amount_prompt)

        def check_bet_amount(m):
            return (
                    m.author == message.author and
                    m.channel == message.channel and
                    m.content.isdigit()
            )

        while True:
            try:
                bet_message = await client.wait_for('message', check=check_bet_amount, timeout=30.0)
                bet_amount = int(bet_message.content)
                if bet_amount == 1:
                    bet_amount = 1000
                # 사용자의 현재 포인트 가져오기
                user_points = get_user_points(client.connection, discord_id)

                # 베팅 금액이 사용자의 포인트보다 많은지 확인
                if bet_amount > user_points:
                    await message.channel.send('잘못된 베팅 금액입니다. 다시 입력해주세요.')
                    continue  # 다시 입력 받음
                break  # Valid bet amount received, break out of the loop
            except asyncio.TimeoutError:
                await message.channel.send('시간초과입니다. 다시 시도해주세요.')
                return
            except ValueError:
                # This exception handles non-integer inputs
                await message.channel.send('잘못된 베팅 금액입니다. 다시 입력해주세요.')
        # 베팅 금액이 유효하게 입력되었을 때
        if bet_amount is not None:
            # 포인트 차감
            deduction_successful, new_points = deduct_points(client.connection, discord_id, bet_amount)

            if deduction_successful:
                # 포인트 차감 성공 처리
                await message.channel.send(f"베팅이 완료되었습니다. 남은 포인트: {new_points}포인트")
                # 여기에 이후 처리 로직 추가 (예: betting_predictions에 베팅 정보 추가, DB에 저장 등)
            else:
                # 포인트가 부족한 경우 처리
                await message.channel.send("포인트가 부족합니다.")
                return
        else:
            # 베팅 금액이 유효하지 않은 경우 처리
            return

        selected_team = int(team_choice.content) - 1  # 선택한 팀 인덱스
        bet_amount_value = bet_amount
        potential_earnings = int(bet_amount_value * odds[selected_team]) if odds[selected_team] else 0
        betting_predictions.append((team_choice.content, bet_amount, potential_earnings))
        match_id = (current_week - 1) * 10 + i + 1
        team_choice_value = selected_team + 1
        save_success = save_bet(discord_id, current_week, match_id, team_choice_value, bet_amount_value,
                                client.connection)
        if not save_success:
            all_saved_successfully = False
        # 모든 베팅 정보와 예상 수익 출력
    if all_saved_successfully:
        await message.channel.send("DB에 정확히 저장되었습니다.")
    else:
        await message.channel.send("일부 베팅 정보가 DB에 저장되지 않았습니다.")
    for i, prediction in enumerate(betting_predictions):
        selected_team_index = int(prediction[0]) - 1  # 선택한 팀 인덱스 (0 또는 1)
        team_name = week_matches[i][selected_team_index]  # 선택한 팀 이름
        await message.channel.send(
            f"선택한 팀: {team_name} ({prediction[0]}), 베팅 금액: {prediction[1]}, 맞히면 얻는 금액: {prediction[2]}")
async def show_rank(message):
    # 데이터베이스 연결 설정
    connection = create_connection("127.0.0.1", "root", db_password, "lck_betting_db")
    if connection is not None:
        try:
            ranked_users = get_users_ranked_by_points(connection)
            response = "사용자 포인트 순위:\n"
            for rank, (user_id, points) in enumerate(ranked_users, start=1):
                response += f"{rank}등: {user_id}, points {points}\n"
            await message.channel.send(response)
        finally:
            connection.close()
    else:
        await message.channel.send("데이터베이스 연결에 실패했습니다.")
async def handle_weekly_summary(message, connection, odds_list):
    week = get_current_week()
    week_bets = get_all_bets_by_week(connection, week)
    match_results = [2, 1, 2, 1, 1, 2, 2, 2, 2, 2]  # 이번 주 경기 결과

    betting_winnings, result = calculate_betting_results(match_results, odds_list, week_bets)

    # 각 사용자의 포인트를 데이터베이스에 업데이트
    for discord_id, winnings in betting_winnings.items():
        add_success, new_points = add_points(connection, discord_id, winnings)
        if not add_success:
            print(f"Error updating points for Discord ID {discord_id}")

    # 사용자 이름을 가져오기 위한 SQL 쿼리
    def get_user_name(discord_id):
        cursor = connection.cursor()
        query = "SELECT Name FROM Users WHERE DiscordID = %s"
        cursor.execute(query, (discord_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    # 승리 횟수에 따라 사용자의 name으로 정렬
    user_names_with_wins = [(get_user_name(discord_id), wins) for discord_id, wins in result.items()]
    sorted_results = sorted(user_names_with_wins, key=lambda x: x[1], reverse=True)

    response = "이번 주 베팅 결과:\n"

    total_len = len(match_results)

    for discord_id, winning in betting_winnings.items():
        user_name = get_user_name(discord_id)
        response += f"{user_name if user_name else 'Unknown'}: 이득 {int(winning)}, 결과 {result[discord_id]}승 {total_len - result[discord_id]}패\n"

        # 승리 횟수 순으로 사용자 정렬 결과 추가
    response += "\n승리 횟수 순 사용자:\n"
    for user_name, wins in sorted_results:
        response += f"{user_name if user_name else 'Unknown'}: {wins}승\n"

    await message.channel.send(response)
    weekly_summaries.append(response)

async def start_blackjack_game(self, message):
    game = BlackjackGame()
    discord_id = str(message.author.id)
    if not is_user_registered(self.connection, discord_id):
        await message.channel.send("먼저 !register를 이용해서 사용자 등록을 해주세요.")
        return
    # Fetch user's current points (assuming a function exists to do this)
    user_points = get_user_points(self.connection, discord_id)

        # Ask for bet amount
    bet_amount_prompt = f"얼마를 베팅하시겠습니까? 현재 보유 포인트: {user_points}포인트. 베팅 금액으로 1을 입력할 시 기본 금액인 1000이 베팅 됩니다. 금액을 입력해주세요: "
    await message.channel.send(bet_amount_prompt)

    # Wait for player's response and validate bet
    try:
        reply = await self.wait_for('message', check=lambda m: m.author == message.author, timeout=30.0)
        bet_amount = int(reply.content)  # Convert the reply to an integer
        if bet_amount == 1:
            bet_amount = 1000
        if bet_amount > user_points:
            await message.channel.send("포인트가 부족합니다.")
            return
    except asyncio.TimeoutError:
        await message.channel.send("시간 초과입니다.")
        return
    except ValueError:
        await message.channel.send("유효한 숫자를 입력해주세요.")
        return

    # Store the original bet amount for later use
    original_bet_amount = bet_amount
        # Deduct points
    deduction_successful, new_points = deduct_points(self.connection, message.author.id, bet_amount)
    if not deduction_successful:
        await message.channel.send("Failed to deduct points.")
        return

    # 플레이어와 딜러에게 카드 두 장씩 나눠줌
    for _ in range(2):
        game.deal_card(game.player_hand)
        game.deal_card(game.dealer_hand)



    def cards_to_string(cards):
        return ', '.join([f"{card['suit']} {card['rank']}" for card in cards])

    player_score = game.calculate_score(game.player_hand)
    player_cards_str = cards_to_string(game.player_hand)
    # 플레이어와 딜러의 초기 카드 상태를 메시지로 전송
    await message.channel.send(f"당신의 카드: {player_cards_str}, 점수: {player_score}")

    dealer_score = game.calculate_score(game.dealer_hand)
    dealer_cards_str = cards_to_string(game.dealer_hand)

    await message.channel.send(f"딜러의 카드: {dealer_cards_str}, 점수: {dealer_score}")

    # 플레이어의 행동 결정
    player_busted = await game.player_turn(self, game, message)  # 버스트 여부를 반환하도록 수정

    # 플레이어가 버스트되지 않았을 때만 딜러의 행동 결정
    if not player_busted:
        await game.dealer_turn(message)

    # Determine game outcome and award points if the player wins
    game_result = await game.announce_winner(game, message)  # Ensure this method returns the game result
    # Check if the player won and award winnings
    if game_result == "플레이어의 승리입니다.":  # Replace "player_wins" with the actual winning condition
        winning_amount = original_bet_amount * 2
        addition_successful, new_total_points = add_points(self.connection, message.author.id, winning_amount)
        if addition_successful:
            await message.channel.send(
                f" {winning_amount} 포인트 획득. 현재 점수는 {new_total_points} 포인트입니다.")
        else:
            await message.channel.send("에러로 인해 포인트 획득을 실패했습니다.")
async def attendance_check(connection, discord_id, message):
    today = datetime.now().date()

    # Check if the user already checked in today
    cursor = connection.cursor()
    query = "SELECT * FROM Attendance WHERE DiscordID = %s AND DateChecked = %s"
    cursor.execute(query, (discord_id, today))
    attendance_record = cursor.fetchone()

    if attendance_record:
        # User has already checked in today
        await message.channel.send("오늘 이미 출석체크를 했습니다.")
    else:
        # User has not checked in today, insert record and add points
        insert_query = "INSERT INTO Attendance (DiscordID, DateChecked, Points, Name) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (discord_id, today, 10000, message.author.id))
        connection.commit()

        # Add points to user's account
        add_success, new_points = add_points(connection, discord_id, 10000)
        if add_success:
            await show_current_week_matches(message)
            await message.channel.send(f"포인트가 추가되었습니다. 새로운 포인트: {new_points}")

    cursor.close()