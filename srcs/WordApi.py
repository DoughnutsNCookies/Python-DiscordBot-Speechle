from gtts import gTTS
from bs4 import BeautifulSoup
import requests
import random
import json
import os

URL			= 'https://www.thefreedictionary.com/'
WORDS_PATH	= 'words.txt'

class WordApi:
	def __init__(self):
		with open(WORDS_PATH) as f:
			self.english_words = f.read().splitlines()
		if not self.english_words:
			raise ValueError('No English words found in ' + WORDS_PATH)
		self.word = None
		self.definition	= None
		self.sentence = None
	
	def generate_word(self):
		while True:
			try:
				self.word = random.choice(self.english_words).lower()
				response = requests.get(URL + self.word)
				if (response.status_code == 200):
					soup = BeautifulSoup(response.text, 'html.parser')
					extracted = soup.find('div', {'class': 'ds-list'}).text.strip().split(':')
					self.definition = "".join([extracted[0], extracted[0][:-1]][extracted[0][-1] == '.'].split('.')[-1].strip())
					break
				else:
					print(f'Failed to retrieve the definition for {self.word}: {response.status_code}')
			except Exception as err:
				print(f'Error: {err}: {self.word}')
	
	def generate_definition(self):
		tts = gTTS(text=self.definition, lang='en')
		tts.save(self.word + '-definition.mp3')
	
	def generate_sentence(self):
		tts = gTTS(text=self.sentence, lang='en')
		tts.save(self.word + '-sentence.mp3')

	def cleanup(self):
		try:
			os.remove(self.word + '-audio.mp3')
			os.remove(self.word + '-definition.mp3')
			os.remove(self.word + '-sentence.mp3')
		except FileNotFoundError():
			pass