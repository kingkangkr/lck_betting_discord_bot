import random
import asyncio
from utils import *
from texts import matches
from get_odds_of_matches import odds_list
from blackjack import BlackjackGame
#from math_question import generate_math_question

weekly_summaries = []
async def play_game(message):
    choices = ['가위', '바위', '보']
    bot_choice = random.choice(choices)
    await message.channel.send(f'봇이 선택한 것은 {bot_choice}입니다!')



async def register_user(client, message):

