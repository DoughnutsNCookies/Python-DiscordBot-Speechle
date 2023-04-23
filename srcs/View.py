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
		self.wordApi.generate_definition()
		with open (self.wordApi.word + '-definition.mp3', 'rb') as f:
			file = discord.File(f, filename='definition.mp3')
			await self.channel.send(file=file)
		self.wordApi.cleanup()
		await interaction.response.edit_message(view=self)