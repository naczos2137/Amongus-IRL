import random
from enum import Enum

import discord

import Buttons
import Config
import Game


class Player:
    def __init__(self, discord_object: discord.Member, game: Game):
        self.role = "Innocent"
        self.perks = []
        self.discord_object = discord_object
        self.game = game
        self.task = ""
        self.game_message = None

    def new_task(self):
        self.task = random.choice(Config.Tasks).replace('{RANDOM_USER}',
                                                        random.choice(self.game.players_alive).discord_object.name)

    async def send_game_message(self):
        embed = discord.Embed(title=f'Witaj {self.discord_object.name}', description='Gracze: \n' + ' '.join(
            f'{player.discord_object.name}' for player in self.game.players_alive) + f'\nTask: {self.task}')
        if self.game_message is None:
            game_buttons = Buttons.GameButtons(player=self, game=self.game)
            self.game_message = await Game.send(self.discord_object, embed=embed, view=game_buttons)
        else:
            await self.game_message.edit(embed=embed)

    async def perk_getter(self, button):
        r = random.randint(0, 4)
        if r == 0:
            match self.role:
                case 'Innocent':
                    self.perks.append()
                case 'Traitor':
                    pass
        await button.response.send_message(f'nie dostałeś żandego perka (nie zaprogramowałem jeszcze perków)', ephemeral=True)

    def __str__(self):
        return self.discord_object.name
