import config
import logging
import json
from datetime import datetime

from google.appengine.api import urlfetch
from django.template.defaultfilters import slugify

class EvolveItemConverter(object):

	def __init__(self, json):
		self.json = json
		self.challenge = {}
		self.data = []
		self._process_challenge_info()
		self._process_challenge_data()
	
	def _process_challenge_info(self):
		for key in self.json:
			if key == 'Configuration':
				for key_config in self.json[key]:
					if config.API_TO_DATASTORE.has_key(key_config):
						self.challenge[config.API_TO_DATASTORE[key_config]] = self.json[key][key_config]
			elif config.API_TO_DATASTORE.has_key(key):
				self.challenge[config.API_TO_DATASTORE[key]] = self.json[key]
		
		self._process_challenge_extras()
	
	def _process_challenge_extras(self):
		self.challenge['slug'] = slugify(self.challenge['name'])
		
		for time in ['start', 'end']:
			if self.challenge.has_key(time):
				self.challenge[time] = datetime.utcfromtimestamp(self.challenge[time])
		
		if not self.challenge.has_key('end') and self.challenge.has_key('start'):
			self.challenge['end'] = self.challenge['start'] + config.DEFAULT_CHALLENGE_DURATION
		
		self.challenge['updated'] = datetime.now()
		
		if not self.challenge.has_key('type'):
			self.challenge['type'] = 'versus' if 'vs' in self.challenge['name'] and self.challenge['goal'] == 50 else 'counter'
		
	def _process_challenge_data(self):
		if not self.json.has_key('DataPoints') or not len(self.json['DataPoints']):
			return
		
		previous = 0.0
		start = self.challenge['start']
		end = self.challenge['end'] + config.DEFAULT_CHALLENGE_POST_DELAY
		
		for point in self.json['DataPoints']:
			value = point['Value']
			new = {
				'updated': datetime.strptime(point['DateTime'], config.STRIP_TIME_BASE),
				'value': value,
				'increment': value - previous
			}
			
			if new['updated'] < start or new['updated'] > end:
				continue
				
			previous = value
			self.data.append(new)
			self.challenge['progress'] = value


class EvolveItem(EvolveItemConverter):

	def __init__(self, json):
		super(self.__class__, self).__init__(json)
		self.id = self.challenge['id']
		self.slug = self.challenge['slug']
		self.progress = self.challenge['progress']
		self.db = None
	
	def to_dict(self, exclude=['data']):
		_dict = self.challenge
		for item in exclude:
			if _dict.has_key(item):
				del _dict[item]
		return _dict


class EvolveBatch(object):
	
	def __init__(self, challenge_id=None):
		self.id = challenge_id
		self.challenges = []
		self.ids = []

	def fetch(self):
		url = self.__get_url()
		result = urlfetch.fetch(url)
		if result.status_code != 200 or result.content is None:
			logging.error('Unable to retrieve challenge API. URL requested replied with %s: %s' % (result.status_code, url))
			return []
		logging.info('Successfully retrieved challenge API: %s' % url)
	
		for challenge in self.__parse(result.content):
			self.challenges.append(EvolveItem(challenge))
		for challenge in self.challenges:
			self.ids.append(challenge.id)
		return self.challenges
		
	def __parse(self, result):
		challenges = json.loads(result)
		if type(challenges) is not list:
			challenges = [challenges]
		return challenges
		
	def __get_url(self):
		url = config.URL_API_EVOLVE_CHALLENGE
		
		if self.id is not None:
			return '%s%s' % (url, self.id)
		return url