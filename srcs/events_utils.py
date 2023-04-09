from WordApi import WordApi
import discord
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
	await message.reply("Room-" + message.author.discriminator + " created! Hop on over!")

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

async def start_game(message):
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	if not channel:
		return
	await channel.send(f"Welcome to Speechle! You will be given an audio file to listen and your goal is to transcribe it into text.\n```MARKDOWN\n# Important information\n-> Your time limit is 30 seconds per word\n-> Max amount of points you can get from each word is 3 points\n-> Each hint you use reduces the points by 1\n-> You only get one attempt per word\n# Hints\n-> Definition: Provides a definition of the word\n-> Example: Uses the word in a sentence\n```\nScore as high as you can! Good luck and have fun!")
	try:
		wordApi = WordApi()
		await channel.send("Generating word...")
		wordApi.generate_word()
		with open (wordApi.word + '-audio.mp3', 'rb') as f:
			file = discord.File(f, filename='audio.mp3')
			await channel.send(file=file)
		await channel.send(f"Word: {wordApi.word}\nDefinition: {wordApi.definition}\nCharacters: {wordApi.characters}")
		wordApi.cleanup()
	except Exception as e:
		print(e)
