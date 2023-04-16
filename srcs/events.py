from events_utils import create_channel, delete_channel, start_game
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
	if message.content == 's!start':
		await delete_channel(message)
		await create_channel(message)
		await start_game(bot, message)
	if message.content == 's!stop':
		await delete_channel(message)
	if message.content == 's!leaderboard':
		print(message.author.id)