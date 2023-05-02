from events_utils import permission_denied, show_help, create_channel, delete_channel, start_game, show_stats, show_leaderboard
import random
import discord
import re

async def estart(bot):
	await bot.change_presence(activity=discord.Game('with your mom | s!help'))
	print(f'{bot.user} has connected to Discord!')

async def emessage(bot, message):
	if message.author == bot.user:
		return
	if re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator == message.channel.name and message.content.startswith('s!'):
		return await permission_denied(message)
	if message.content == 's!help':
		await show_help(message)
	if message.content == 's!start':
		await delete_channel(message)
		await create_channel(message)
		await start_game(bot, message)
	if message.content == 's!stop':
		await delete_channel(message)
	if message.content == 's!stats':
		await show_stats(message)
	if message.content == 's!leaderboard':
		await show_leaderboard(bot, message)
	if "yes or no" in message.content.lower() or "true or false" in message.content.lower():
		await message.reply(["Yes of course", "No you donkey"][random.randint(0,1)])
	elif "true" in message.content.lower() or "truth" in message.content.lower():
		await message.reply("So true!")
	elif "false" in message.content.lower():
		await message.reply("Yep that's :billed_cap:")
	elif "onz" in message.content.lower() or "mou" in message.content.lower():
		await message.reply("Onz")
