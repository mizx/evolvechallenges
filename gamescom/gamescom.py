import time
import json
import urllib2
import datetime

API = 'https://api.twitch.tv/kraken/streams/evolvegame'
id = '-3.txt'
directory = 'F:/Google Drive/evolve/'
#API = 'https://api.twitch.tv/kraken/streams/dota2ti'

SLEEP = 60*5

def fetch_and_write():
	try:
		data = json.load(urllib2.urlopen(API))
		if data.has_key('stream') and data['stream'] and data['stream'].has_key('viewers'):
			data_json = {
				'DateTime': datetime.datetime.now().isoformat().partition('.')[0],
				'Value': data['stream']['viewers']
			}
			with open(directory + id, 'a') as outfile:
				json.dump(data_json, outfile)
				outfile.write(',\n')
		else:
			print 'Stream is offline'
	except:
		print 'An error occured while pulling request or parsing'
	
	time.sleep(SLEEP)

def check():
	while True:
		fetch_and_write()

check()