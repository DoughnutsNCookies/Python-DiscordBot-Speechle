from dotenv import load_dotenv
from discord.ext import commands
from commands import cping
from events import estart, emessage
import discord
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='s!', case_insensitive=True, intents=discord.Intents.all())

@bot.event
async def on_ready():
	await estart(bot)

@bot.event
async def on_message(message):
	await emessage(bot, message)

@bot.tree.command(name="ping")
async def ping(interaction):
	await cping(bot, interaction)


bot.run(TOKEN)