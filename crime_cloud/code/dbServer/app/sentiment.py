#!/usr/bin/env python3

import sys
import json
from textblob import TextBlob 

class SentimentAnalysis(object): 

	def analysisText(self, text): 
	
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(text)

		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def sentimentAnalysis(self, tweet): 
		tweet['sentiment'] = self.analysisText(tweet["text"])
		return tweet



if __name__ == "__main__": 
	text = "I am fucking stupid"
	senti = SentimentAnalysis().analysisText

	print(senti(text))
