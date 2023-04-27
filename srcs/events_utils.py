from WordApi import WordApi
from View import MyView
from replit import db
import asyncio
import discord
import time
import re

CATEGORY_NAME = "Speechle"
TIME_BUFFER = 1
TIMEOUT = 30
BONUS_TIMEOUT = 15

async def permission_denied(message):
	await message.channel.send(embed=discord.Embed(title="You can't use Speechle commands in a Speechle room!", color=discord.Color.red()))

async def show_help(message):
	await message.reply(embed=discord.Embed(title="Commands available", description="``s!start``\nStarts a game of Speechle\n\n``s!stop``\nStops your game of Speechle\n\n``s!stats``\nShows your Speechle stats\n\n``s!leaderboard``\nShows the leaderboard", color=discord.Color.blurple()))

async def create_channel(message):
	channelName = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator

	category = discord.utils.get(message.guild.categories, name=CATEGORY_NAME)
	if not category:
		category = await message.guild.create_category(CATEGORY_NAME, position=message.channel.category.position)

	overwrites = {
		message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
		message.guild.me: discord.PermissionOverwrite(read_messages=True),
		message.author: discord.PermissionOverwrite(read_messages=True)}

	await category.create_text_channel(channelName, overwrites=overwrites)
	await message.reply(embed=discord.Embed(title="Room created!", description=f"{channelName} room created! Hop on over!", color=discord.Color.green()))

async def delete_channel(message):
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator

	category = discord.utils.get(message.guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	while channel:
		await channel.delete()
		channel = discord.utils.get(category.text_channels, name=channel_name)	
	if len(category.text_channels) == 0:
		await category.delete()

async def start_game(bot, message):
	async def update_message(wordApi, myView, sentView, channel, myEmbed, myTitle):
		myView.button.disabled = True
		await sentView.edit(view=myView, embed=myEmbed)
		await channel.send(embed=discord.Embed(title=myTitle, description=[f"The word was ``{wordApi.word}``.\nDefinition: ``{wordApi.definition}``.\nBetter luck next time! Type ``s!start`` outside of this room to play again to start a new game!", ""][myTitle == "Correct!"], color=[discord.Color.red(), discord.Color.green()][myTitle == "Correct!"]))

	def update_database(id, totalScore, totalTime, totalWord):
		try:
			db[id + "-game"] += 1
			db[id + "-score"] = max(db[id + "-score"], totalScore)
			db[id + "-time"] += totalTime
			db[id + "-word"] += totalWord
		except KeyError:
			db[id + "-game"] = 1
			db[id + "-score"] = totalScore
			db[id + "-time"] = totalTime
			db[id + "-word"] = totalWord

	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	category = discord.utils.get(message.guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	if not channel:
		return
	await channel.send(embed=discord.Embed(title="Welcome to Speechle!", description="You will be given an audio file to listen and your goal is to transcribe it into text.\nScore as high as you can! Good luck and have fun!", color=discord.Color.green()))
	await channel.send("```MARKDOWN\n# Important\n-> Your time limit is 30 seconds per word\n-> You only get 1 attempt per word\n-> Max amount of points you can get from each word is 3 points\n# Points\n-> 1 point for a correct transcription\n-> 1 point for a correct transcription under 15 seconds\n-> 1 point for not using hint\n# Hints\n-> Definition: Provides a definition of the word\n```")
	try:
		wordApi = WordApi()
		totalScore = 0
		totalTime = 0
		totalWord = 0
		while True:
			score = [3]
			await channel.send("Generating word...")
			wordApi.generate_word()
			with open (wordApi.word + '.mp3', 'rb') as f:
				myFile = discord.File(f, filename='audio.mp3')
			myView = MyView(channel, wordApi, score)
			sentView = await channel.send(file=myFile, view=myView, embed=discord.Embed(title=f"Time runs out <t:{int(time.time()) + TIMEOUT + TIME_BUFFER}:R>", color=discord.Color.blurple()))
			wordApi.cleanup()
			try:
				startTime = time.perf_counter()
				message = await bot.wait_for('message', check=lambda received: received.author == message.author and received.channel == channel, timeout=(TIMEOUT))
			except asyncio.TimeoutError:
				update_database(str(message.author.id), totalScore, totalTime, totalWord)
				return await update_message(wordApi, myView, sentView, channel, discord.Embed(title=f"Final score: {totalScore}", description=f"Time: {TIMEOUT}.00 seconds", color=discord.Color.red()), "Time's up!")
			if message.content.upper() == wordApi.word.upper():
				elapsedTime = time.perf_counter() - startTime
				score[0] -= (elapsedTime > BONUS_TIMEOUT)
				totalScore += score[0]
				totalTime += elapsedTime
				totalWord += 1
				await update_message(wordApi, myView, sentView, channel, discord.Embed(title=f"Current score: {totalScore}", description=f"Time: {round(elapsedTime, 2)} seconds", color=discord.Color.green()), "Correct!")
			else:
				update_database(str(message.author.id), totalScore, totalTime, totalWord)
				return await update_message(wordApi, myView, sentView, channel, discord.Embed(title=f"Final score: {totalScore}", description=f"Time: {round(time.perf_counter() - startTime, 2)} seconds", color=discord.Color.red()), "Incorrect!")
	except Exception as e:
		await channel.send(embed=discord.Embed(title="Something broke again, please try again later :smiling_face_with_tear:", description=f"Error: {str(e)}", color=discord.Color.red()))

async def show_stats(message):
	try:
		games = db[str(message.author.id) + "-game"]
		score = db[str(message.author.id) + "-score"]
		time = db[str(message.author.id) + "-time"]
		words = db[str(message.author.id) + "-word"]
		aWPG = round(words / games, 2)
		aTPW = 0
		if words > 0:
			aTPW = round(time / words, 2)
		aTPG = round(time / games, 2)
		await message.reply(embed=discord.Embed(title="Your Speechle stats", description=f"Games played: **{games}**\nHighest score: **{score}**\nTotal time played: **{round(time, 2)}s**\nTotal words transcribed: **{words}**\n\nAverage words transcribed per game: **{aWPG}**\nAverage time per word: **{aTPW}s**\nAverage time per game: **{aTPG}s**", color=discord.Color.green()))
	except KeyError:
		await message.reply(embed=discord.Embed(title="No data found!", description="Use ``s!start`` to start a game!"))

async def show_leaderboard(bot, message):
	keys = db.keys()
	database = {}
	for key in keys:
		if key.endswith("-score"):
			database[key[:-6]] = db[key]
	sortedDatabase = sorted(database.items(), key=lambda x: x[1], reverse=True)
	try:
		authorRank = sortedDatabase.index((str(message.author.id), database[str(message.author.id)]))
	except KeyError:
		authorRank = -1
	while len(sortedDatabase) > 10:
		sortedDatabase.pop()
	description = ""
	for i, userData in enumerate(sortedDatabase):
		try:
			userName = await bot.fetch_user(userData[0])
		except discord.errors.NotFound:
			userName = "unknown"
		description += f"**{i + 1}**: **{userName}** - **{userData[1]}**\n"
	if authorRank != -1:
		description += f"**--------------------**\n**{authorRank + 1}**: **{message.author.name + '#' + message.author.discriminator}** - **{db[str(message.author.id) + '-score']}**"
	await message.reply(embed=discord.Embed(title="Leaderboards", description=description, color=discord.Color.blurple()))
