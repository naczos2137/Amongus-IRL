import random
from typing import List, Dict

import discord
from discord import player

import Buttons
import Config
from Player import Player


async def send(player: discord.Member, message: str = '', embed=None, view=None):
    return await player.send(message, embed=embed, view=view)


class Game:
    def __init__(self):
        self.players_alive: List[Player] = []
        self.players: List[Player] = []
        self.traitors: List[Player] = []
        # self.votes: Dict[Player, int] = {}
        self.EM = None

    async def start(self, dc_obj_players: List[discord.Member]):
        for dc_obj in dc_obj_players:
            self.players.append(Player(dc_obj, game=self))
            self.players_alive = list(self.players)
        for player in random.sample(self.players_alive, k=Config.Traitors):
            player.role = "Traitor"
            self.traitors.append(player)
        for player in self.players_alive:
            player.new_task()
            await player.send_game_message()

    async def kill(self, player: Player):
        self.players_alive.remove(player)
        if player in self.traitors:
            self.traitors.remove(player)
        if len(self.players_alive) == len(self.traitors):
            await self.end(winner="Traitorów")
        elif len(self.traitors) == 0:
            await self.end(winner="Innocentów")

    async def end(self, winner: str):
        embed = discord.Embed(title=f'Wygrał team {winner}', colour=discord.Color.yellow())
        for player in self.players:
            if player in self.players_alive:
                await player.game_message.delete()
            await send(player.discord_object, embed=embed)


