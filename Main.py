import asyncio

from discord import app_commands
import discord
from discord.ext import commands
import time
import Buttons
import Config
from Game import Game

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')
    try:
        synced = await bot.tree.sync()
        print(f'Synced: {len(synced)} commands')
    except Exception as e:
        print(e)


@bot.tree.command(name="start")
async def start(interaction: discord.Interaction):
    embed = discord.Embed(title=f'Start nowej gry <t:{int(time.time()) + Config.LobbyTime}:R>', description="Kliknij przycisk by dołączyć",
                          colour=discord.Colour.blue())
    join_button = Buttons.JoinGameButton()
    await interaction.response.send_message(embed=embed, view=join_button)
    await asyncio.sleep(Config.LobbyTime)
    embed = discord.Embed(title="Start Gry",
                          description=f'Zobaczcie PV (nikomu innemu nie pokazujcie) \nGraczy: {len(join_button.dc_obj_players)} \nTraitorów: {Config.Traitors}')
    await interaction.followup.send(embed=embed)
    game = Game()
    await game.start(join_button.dc_obj_players)



bot.run('TOKEN')
