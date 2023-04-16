import discord

async def cping(bot, interaction):
	await interaction.response.send_message(embed=discord.Embed(title="Pong!", description=f'Latency: {round(bot.latency * 1000)}ms', color=discord.Color.green()))