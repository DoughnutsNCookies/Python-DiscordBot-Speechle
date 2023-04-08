import discord

async def cping(bot, interaction):
	embed = discord.Embed(
		title="Pong!",
		description=f'Latency: {round(bot.latency * 1000)}ms',
		color=discord.Color.green())
	await interaction.response.send_message(embed=embed)