from WordApi import WordApi
import asyncio
import discord
import time
import re

CATEGORY_NAME = "Speechle"

async def create_channel(message):
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		category_position = message.channel.category.position
		category = await guild.create_category(CATEGORY_NAME, position=category_position)

	overwrites = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False),
		guild.me: discord.PermissionOverwrite(read_messages=True),
		message.author: discord.PermissionOverwrite(read_messages=True)}

	new_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
	await message.reply(re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator + " room created! Hop on over!")

async def delete_channel(message):
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	while channel:
		await channel.delete()
		channel = discord.utils.get(category.text_channels, name=channel_name)	
	if len(category.text_channels) == 0:
		await category.delete()

async def start_game(bot, message):
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	if not channel:
		return
	await channel.send(f"**Welcome to Speechle!** You will be given an audio file to listen and your goal is to transcribe it into text.\n```MARKDOWN\n# Important\n-> Your time limit is 30 seconds per word\n-> You only get 1 attempt per word\n-> Max amount of points you can get from each word is 3 points\n# Points\n-> 1 point for a correct transcription\n-> 1 point for a correct transcription under 10 seconds\n-> 1 point for not using hint\n# Hints\n-> Definition: Provides a definition of the word\n```Score as high as you can! Good luck and have fun!")
	try:
		wordApi = WordApi()
		while True:
			await channel.send("Generating word...")
			wordApi.generate_word()
			with open (wordApi.word + '-audio.mp3', 'rb') as f:
				file = discord.File(f, filename='audio.mp3')
				await channel.send(file=file)
			await channel.send(f"Word: {wordApi.word}\nDefinition: {wordApi.definition}\n")
			wordApi.cleanup()
			try:
				start_time = time.monotonic()
				message = await bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == channel, timeout=30)
				duration = time.monotonic() - start_time
			except asyncio.TimeoutError:
				return await channel.send("**Time's up!** The word was ``" + wordApi.word + "``. Better luck next time! Type ''s!start'' outside of this room to play again to start a new game!")
			if message.content == wordApi.word:
				await channel.send("**Correct!**")
			else:
				return await channel.send("**Incorrect!** The word was ``" + wordApi.word + "``. Better luck next time!\nType ``s!start`` outside of this room to play again to start a new game!")
	except Exception as e:
		print(e)
