from discord.ui import View, Button
import discord

class MyView(View):
	def __init__(self, channel, wordApi, score):
		super().__init__()
		self.channel = channel
		self.wordApi = wordApi
		self.button = Button(label="Definition Hint", style=discord.ButtonStyle.blurple)
		self.button.callback = self.on_button_click
		self.add_item(self.button)
		self.score = score

	async def on_button_click(self, interaction: discord.Interaction):		
		self.button.disabled = True
		self.score[0] -= 1
		await self.channel.send(embed=discord.Embed(title="Definition", description=self.wordApi.definition, color=discord.Color.blurple()))
		await interaction.response.edit_message(view=self)