import asyncio
import random

from utils import *


class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.dealer_hand = []
        self.player_hand = []
    def cards_to_string(self, cards):
        return ', '.join([f"{card['suit']} {card['rank']}" for card in cards])
    def create_deck(self):
        suits = ['하트', '다이아', '클로버', '스페이드']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return card

    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        score = 0
        aces = 0  # 에이스 카운트

        for card in hand:
            rank = card['rank']
            score += values[rank]
            if rank == 'A':
                aces += 1

        # 에이스가 있고, 점수가 21을 초과하면 에이스를 1로 간주
        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score

    async def player_turn(self, client, game, message):
        while True:
            await message.channel.send("히트 하시려면 '히트'나 'ㅎㅌ', 스탠드 하시려면 '스탠드'나 'ㅅㅌㄷ'라고 입력해주세요. 시간제한 30초"+ message.author.mention)
            reply = await client.wait_for('message', check=lambda m: m.content in ["히트", "스탠드","ㅎㅌ","ㅅㅌㄷ"] and m.channel == message.channel and m.author == message.author, timeout=30.0)
            if reply.content == "히트" or reply.content == "ㅎㅌ":
                game.deal_card(game.player_hand)
                score = game.calculate_score(game.player_hand)
                player_cards_str = self.cards_to_string(game.player_hand)
                await message.channel.send(f"당신의 카드: {player_cards_str}, 점수: {score}"+ message.author.mention)
                if score > 21:
                    await message.channel.send("버스트! 점수가 21을 넘었습니다."+ message.author.mention)
                    break
            elif reply.content == "스탠드" or reply.content == "ㅅㅌㄷ":
                break

    async def dealer_turn(self, message):
        while self.calculate_score(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
            score = self.calculate_score(self.dealer_hand)
            dealer_cards_str = self.cards_to_string(self.dealer_hand)

            if score > 21:
                await message.channel.send(f"딜러가 버스트했습니다! 딜러의 카드: {dealer_cards_str}, 점수: {score}"+ message.author.mention)
                break

    async def announce_winner(self, game, message):
        player_score = game.calculate_score(game.player_hand)
        dealer_score = game.calculate_score(game.dealer_hand)
        player_cards_str = self.cards_to_string(game.player_hand)
        dealer_cards_str = self.cards_to_string(game.dealer_hand)

        # 딜러의 전체 카드 공개
        await message.channel.send(f"딜러의 카드: {dealer_cards_str}, 점수: {dealer_score}"+ message.author.mention)

        result = "무승부입니다."
        if player_score > 21:
            result = "딜러의 승리입니다."
        elif dealer_score > 21 or player_score > dealer_score:
            result = "플레이어의 승리입니다."
        elif dealer_score > player_score:
            result = "딜러의 승리입니다."

        # 플레이어의 카드 및 게임 결과 공개
        await message.channel.send(f"당신의 카드: {player_cards_str}, 점수: {player_score}"+ message.author.mention)
        await message.channel.send(f"게임 결과: {result}"+ message.author.mention)
        return result





