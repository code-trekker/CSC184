import json

credentials = {}
credentials['CONSUMER_KEY'] = '...'  
credentials['CONSUMER_SECRET'] = '...'  
credentials['ACCESS_TOKEN'] = 	'...' 
credentials['ACCESS_SECRET'] = '...'

with open("twitter_credentials.json", "w") as file:
	json.dump(credentials, file)