from events_utils import create_channel, delete_channel
import discord

async def estart(bot):
	await bot.change_presence(activity=discord.Game('with your mom | s!help'))
	print(f'{bot.user} has connected to Discord!')

async def emessage(bot, message):
	if message.author == bot.user:
		return
	if message.content == 's!start':
		await create_channel(message)
	if message.content == 's!stop':
		await delete_channel(message)