from gtts import gTTS
import requests
import random
import json
import os

API			= 'https://api.dictionaryapi.dev/api/v2/entries/en/'
WORDS_PATH	= 'words.txt'

class WordApi:
	def __init__(self):
		self.word = None
		self.definition	= None
		self.sentence = None
	
	def generate_word(self):
		try:
			with open(WORDS_PATH) as f:
				english_words = f.read().splitlines()
			if not english_words:
				raise ValueError('No English words found in ' + WORDS_PATH)
			while True:
				word = random.choice(english_words)
				response = requests.get(API + word)
				if (response.status_code == 200):
					data = response.json()
					self.word = data[0].get('word')
					return
					# for i in range(len(data[0].get('meanings'))):
					# 	self.definition = data[0].get('meanings')[i].get('definitions')[0].get('definition')
					# 	self.sentence = data[0].get('meanings')[i].get('definitions')[0].get('example')
					# 	if self.word and self.definition and self.sentence:
					# 		print("Audio file generated")
					# 		tts = gTTS(text=self.word, lang='en')
					# 		tts.save(self.word + '-audio.mp3')
					# 		return 
				else:
					print(f'Failed to retrieve the information for {word}: {response.status_code}')
		except requests.exceptions.HTTPError as err:
			print(f'Failed to retrieve the information for {word}: {err}')
		except Exception as err:
			print(f'Error: {err}')
	
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