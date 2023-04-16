from events_utils import create_channel, delete_channel, start_game
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
	if message.content == 's!me':
		try:
			games = db[str(message.author.id) + "-game"]
			score = db[str(message.author.id) + "-score"]
			time = db[str(message.author.id) + "-time"]
			words = db[str(message.author.id) + "-word"]
			await message.reply(embed=discord.Embed(title="Your Speechle stats", description=f"Games played: {games}\nHighest score: {score}\nTotal time played: {round(time, 2)}\nTotal words transcribed: {words}\n\nAverage words transcribed per game: {round(words / games, 2)}\nAverage word per game: {round(words / games, 2)}\nAverage time per word: {round(time / games, 2)}", color=discord.Color.green()))
		except KeyError:
			await message.reply("No data found! Use ``s!start`` to start a game!")
	if message.content == 's!clear':
		for key in db.keys():
			del db[key]