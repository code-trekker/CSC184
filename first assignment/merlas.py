from twython import Twython, TwythonStreamer
import json
import csv
import pandas as pd

with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

#creating an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

#creating a query for searching
word = raw_input("Enter a keyword: ")
query= {'q': word,
		'result_type':'popular',
		'count': 10,
		'lang': 'en',
		} 	


dict_ = {'user':[], 'date':[], 'text':[], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
	dict_['user'].append(status['user']['screen_name'])
	dict_['date'].append(status['created_at'])
	dict_['text'].append(status['text'])
	dict_['favorite_count'].append(status['favorite_count'])

df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
print df.head(10)	


#tweeting something

t = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
			creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

twit = raw_input("Post a tweet: ")

t.update_status(status=twit)



#streaming tweets now
keys = raw_input("Enter keyword to look for: ")

def process_tweet(tweet):
	d = {}
	d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
	d['text'] = tweet['text'].encode('utf-8')
	d['user'] = tweet['user']['screen_name'].encode('utf-8')
	d['user_loc'] = tweet['user']['location']
	return d


class MyStream(TwythonStreamer):

	def on_success(self, data):
		if data['lang']	== 'en':
			tweet_data = process_tweet(data)
			print tweet_data
			self.save_to_csv(tweet_data)

	def on_error(self, status_code, data):
		print(status_code, data)
		self.disconnect()

	def save_to_csv(self, tweet):
		with open(r'saved_tweets.csv', 'a')	as file:
			writer = csv.writer(file)
			writer.writerow(list(tweet.values()))

stream = MyStream(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
					creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

iterator = stream.statuses.filter(track=keys)


