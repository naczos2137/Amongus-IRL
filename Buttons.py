import asyncio
from typing import List

import discord
import time

from discord.ext import commands

import Config
import Game
import Player
from EM import EM


class JoinGameButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.dc_obj_players = set()
        self.start_time = time.time() + Config.LobbyTime

    @discord.ui.button(label="Dołącz", style=discord.ButtonStyle.primary, emoji="😎", )
    async def button_callback(self, button, interaction):
        if button.user in self.dc_obj_players:
            await button.response.send_message(
                f'Już dołączono do gry', ephemeral=True)
        elif time.time() > self.start_time:
            await button.response.send_message(f'Gra się już rozpoczeła', ephemeral=True)
        else:
            self.dc_obj_players.add(button.user)
            await button.response.send_message(f'Dołączono do gry', ephemeral=True)


class DeleteMessage(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.message = None  # remember to set message

    @discord.ui.button(label="Usuń wiadomość", style=discord.ButtonStyle.primary, emoji="❌")
    async def button_callback(self, button, interaction):
        await self.message.delete()


class GameButtons(discord.ui.View):
    def __init__(self, player: Player.Player, game: Game.Game):
        super().__init__()
        self.player = player
        self.game = game

    @discord.ui.button(label="Task zrobiony", style=discord.ButtonStyle.success)
    async def button_task(self, button, interaction):
        if Config.dev_mode: print(self.player, "task zriobiony")
        self.player.new_task()
        await self.player.perk_getter(button=button)
        await self.player.send_game_message()

    @discord.ui.button(label="Rola", style=discord.ButtonStyle.primary)
    async def button_role(self, button, interaction):
        if Config.dev_mode: print(self.player, "rola")
        await button.response.send_message(f'Jesteś {self.player.role}' + (f'. Team: {" ".join(str(traitor) for traitor in self.game.traitors)}' if self.player.role == 'Traitor' else ''), ephemeral=True)

    @discord.ui.button(label="Nie żyje", style=discord.ButtonStyle.danger)
    async def button_dead(self, button, interaction):
        if Config.dev_mode: print(self.player, "nie zyje")
        await self.game.kill(self.player)
        embed = discord.Embed(title="F bratku")
        em_button = EMButton(player=self.player, game=self.game)
        await self.player.game_message.delete()
        await Game.send(self.player.discord_object, embed=embed, view=em_button)

    @discord.ui.button(label="test", style=discord.ButtonStyle.danger)
    async def button_emergency(self, button, interaction):
        if Config.dev_mode: print(self.player, "test")
        view = EMButton(player=self.player, game=self.game)
        await Game.send(self.player.discord_object, message="pies", view=view)


class EMButton(discord.ui.View):
    def __init__(self, player: Player.Player, game: Game.Game):
        super().__init__()
        self.player = player
        self.game = game

    @discord.ui.button(label="Emergency meeting", style=discord.ButtonStyle.danger)
    async def button_emergency(self, button, interaction):
        if Config.dev_mode: print(self.player, "EM")
        embed = discord.Embed(title=f'️⚠️Emergency meeting⚠️', description=f'Limit czasu: <t:{int(time.time()) + Config.EMTime}:R>', colour=discord.Color.dark_red())
        view = VoteList(game=self.game)
        self.game.EM = EM(game=self.game)
        await self.game.EM.timer()
        for player in self.game.players_alive:
            await player.game_message.delete()
            await Game.send(player.discord_object, embed=embed, view=view)


class VoteList(discord.ui.View):
    def __init__(self, game: Game.Game):
        super().__init__()
        self.game = game

        # Tworzymy opcje selecta w konstruktorze
        self.select_options = [discord.SelectOption(label=str(player)) for player in self.game.players_alive]

        # Dodajemy select do widoku w konstruktorze
        select = discord.ui.Select(placeholder="Na kogo głosujesz...", min_values=1, max_values=1,
                                        options=self.select_options, custom_id="vote_select")
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_option = interaction.data['values'][0]
        print(f'You voted for: {selected_option}')

    def players_select_options(self):
        return [discord.SelectOption(label=str(player)) for player in self.game.players_alive]
