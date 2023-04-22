from events_utils import create_channel, delete_channel, start_game, show_stats
from replit import db
import discord
import re

async def estart(bot):
	await bot.change_presence(activity=discord.Game('with your mom | s!help'))
	print(f'{bot.user} has connected to Discord!')

async def emessage(bot, message):
	if message.author == bot.user:
		return
	if re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator == message.channel.name and message.content.startswith('s!'):
		return await message.channel.send("You can't use Speechle commands in a Speechle room!")
	if message.content == 's!help':
		await message.reply("``s!start``: Starts a game of Speechle\n``s!stop``: Stops a game of Speechle\n``s!me``: Shows your Speechle stats\n``s!clear``: Clears your Speechle stats")
	if message.content == 's!start':
		await delete_channel(message)
		await create_channel(message)
		await start_game(bot, message)
	if message.content == 's!stop':
		await delete_channel(message)
	if message.content == 's!stats':
		await show_stats(message)
	if message.content == 's!clear':
		for key in db.keys():
			del db[key]