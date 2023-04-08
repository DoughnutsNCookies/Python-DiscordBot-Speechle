import discord
import re

async def create_channel(message):
	category_name = "Speechle"
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=category_name)
	if not category:
		category_position = message.channel.category.position
		category = await guild.create_category(category_name, position=category_position)

	overwrites = {
		guild.default_role: discord.PermissionOverwrite(read_messages=False),
		guild.me: discord.PermissionOverwrite(read_messages=True),
		message.author: discord.PermissionOverwrite(read_messages=True)}

	new_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
	await message.reply("Room-" + message.author.discriminator + " created! Hop on over!")

async def delete_channel(message):
	category_name = "Speechle"
	channel_name = re.sub(r"[^a-z]+", "", message.author.name.lower()) + "-" + message.author.discriminator
	guild = message.guild

	category = discord.utils.get(guild.categories, name=category_name)
	if not category:
		return
	channel = discord.utils.get(category.text_channels, name=channel_name)
	if channel:
		await channel.delete()
	if len(category.text_channels) == 0:
		await category.delete()