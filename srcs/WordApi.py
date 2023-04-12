from gtts import gTTS
from bs4 import BeautifulSoup
import requests
import random
import os

URL			= 'https://www.thefreedictionary.com/'
WORDS_PATH	= 'words.txt'

class WordApi:
	def __init__(self):
		with open(WORDS_PATH) as f:
			self.english_words = f.read().splitlines()
		if not self.english_words:
			raise ValueError('No English words found in ' + WORDS_PATH)
	
	def generate_word(self):
		self.word = None
		self.definition	= None
		while self.definition == None :
			try:
				self.word = random.choice(self.english_words).lower()
				response = requests.get(URL + self.word)
				if (response.status_code == 200):
					soup = BeautifulSoup(response.text, 'html.parser')
					extracted = soup.find('div', {'class': 'ds-list'})
					if extracted:
						extracted = extracted.text.strip().split(':')
						self.definition = "".join([extracted[0], extracted[0][:-1]][extracted[0][-1] == '.'].split('.')[-1].strip())
						tts = gTTS(text=self.word, lang='en')
						tts.save(self.word + '-audio.mp3')
				else:
					print(f'Failed to retrieve the definition for {self.word}: {response.status_code}')
			except Exception as e:
				print(f'Failed to retrieve the definition for {self.word}: {e}')
	
	def generate_definition(self):
		tts = gTTS(text=self.definition, lang='en')
		tts.save(self.word + '-definition.mp3')
	
	def cleanup(self):
		try:
			os.remove(self.word + '-audio.mp3')
			os.remove(self.word + '-definition.mp3')
		except FileNotFoundError:
			pass