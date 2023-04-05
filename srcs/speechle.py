from gtts import gTTS
from WordApi import WordApi
import os

def main():
	wordApi = WordApi()
	print(wordApi.word)
	print(wordApi.definition)
	print(wordApi.sentence)
	tts = gTTS(text=wordApi.word, lang='en')
	tts.save('audio.mp3')

if __name__ == '__main__':
	main()
