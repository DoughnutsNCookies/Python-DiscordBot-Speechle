from WordApi import WordApi
from dotenv import load_dotenv
from discord.ext import commands
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='s!', case_insensitive=True, intents=discord.Intents.all())

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game('with your mom | s!help'))
	print(f'{bot.user} has connected to Discord!')

@bot.tree.command(name="ping")
async def tree_ping(interaction: discord.Interaction):
	embed = discord.Embed(
		title="Pong!",
		description=f'Latency: {round(bot.latency * 1000)}ms',
		color=discord.Color.green())
	await interaction.response.send_message(embed=embed)

bot.run(TOKEN)