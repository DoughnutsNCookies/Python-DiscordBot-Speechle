import requests
import random
import json

API 		= 'https://api.dictionaryapi.dev/api/v2/entries/en/'
WORDS_PATH	= 'words.txt'

class WordApi:
	def __init__(self):
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
					for i in range(len(data[0].get('meanings'))):
						self.definition = data[0].get('meanings')[i].get('definitions')[0].get('definition')
						self.sentence = data[0].get('meanings')[i].get('definitions')[0].get('example')
						if self.word and self.definition and self.sentence:
							return 
				else:
					print(f'Failed to retrieve the definition for {word}: {response.status_code}')
		except requests.exceptions.HTTPError as err:
			print(f'Failed to retrieve the definition for {word}: {err}')
		except Exception as err:
			print(f'Error: {err}')

	def	print_formatted(json_string):
		parsed = json.loads(json_string)
		print(json.dumps(parsed, indent=4, sort_keys=True))
