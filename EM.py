import asyncio
from typing import Dict

from discord import player

import Config
import Game
from Player import Player


class EM:
    def __init__(self, game: Game.Game):
        self.game = game
        self.active = True
        self.votes_left = len(self.game.players_alive)
        self.votes: Dict[Player, int] = {}
        for player in self.game.players_alive:
            self.votes[player] = 0

    def vote(self, player):
        self.votes[player] += 1
        self.votes_left -= 1
        if self.votes_left == 0:
            self.active = False
            self.end_vote()

    async def timer(self):
        await asyncio.sleep(Config.EMTime)
        self.end_vote()

    def end_vote(self):
        if self.active:
            player = max(self.votes, key=self.votes.get)
            print(player)
            self.game.players_alive.remove(player)
            self.game.EM = None
            for player in self.game.players_alive:
                player.send_game_message()