from WordApi import WordApi
from View import MyView
import asyncio
import discord
import time
import re

CATEGORY_NAME = "Speechle"
TIME_BUFFER = 1
TIMEOUT = 10

async def create_channel(message):
	channelName = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		category = await guild.create_category(CATEGORY_NAME, position=message.channel.category.position)

	overwrites = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False),
		guild.me: discord.PermissionOverwrite(read_messages=True),
		message.author: discord.PermissionOverwrite(read_messages=True)}

	new_channel = await category.create_text_channel(channelName, overwrites=overwrites)
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
	async def update_message(myView, sentView, channel, myEmbed, content):
		myView.button.disabled = True
		await sentView.edit(view=myView, embed=myEmbed)
		await channel.send(content)

	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	if not channel:
		return
	await channel.send(f"**Welcome to Speechle!** You will be given an audio file to listen and your goal is to transcribe it into text.\n```MARKDOWN\n# Important\n-> Your time limit is 30 seconds per word\n-> You only get 1 attempt per word\n-> Max amount of points you can get from each word is 3 points\n# Points\n-> 1 point for a correct transcription\n-> 1 point for a correct transcription under 15 seconds\n-> 1 point for not using hint\n# Hints\n-> Definition: Provides a definition of the word\n```Score as high as you can! Good luck and have fun!")
	try:
		wordApi = WordApi()
		while True:
			await channel.send("Generating word...")
			wordApi.generate_word()
			with open (wordApi.word + '-audio.mp3', 'rb') as f:
				myFile = discord.File(f, filename='audio.mp3')
			myView = MyView(channel, wordApi)
			sentView = await channel.send(file=myFile, view=myView, embed=discord.Embed(title=f"Time runs out <t:{int(time.time()) + TIMEOUT + TIME_BUFFER}:R>", color=discord.Color.blurple()))
			wordApi.cleanup()
			await channel.send(f"Word: {wordApi.word}\nDefinition: {wordApi.definition}\n")
			try:
				startTime = time.perf_counter()
				message = await bot.wait_for('message', check=lambda received: received.author == message.author and received.channel == channel, timeout=(TIMEOUT))
			except asyncio.TimeoutError:
				return await update_message(myView, sentView, channel, discord.Embed(title=f"Final time: {TIMEOUT}.00 seconds", color=discord.Color.red()), "**Time's up!** The word was ``" + wordApi.word + "``. Better luck next time! Type ``s!start`` outside of this room to play again to start a new game!")
			if message.content == wordApi.word:
				await update_message(myView, sentView, channel, discord.Embed(title=f"Final time: {round(time.perf_counter() - startTime, 2)} seconds", color=discord.Color.green()), "**Correct!**")
			else:
				return await update_message(myView, sentView, channel, discord.Embed(title=f"Final time: {round(time.perf_counter() - startTime, 2)} seconds", color=discord.Color.red()), "**Incorrect!** The word was ``" + wordApi.word + "``. Better luck next time!\nType ``s!start`` outside of this room to play again to start a new game!")
	except Exception as e:
		return await channel.send(embed=discord.Embed(title="Something broke again, please try again later :')", description=f"Error: {str(e)}", color=discord.Color.red()))
