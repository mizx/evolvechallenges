import config
import errors
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from django.template.defaultfilters import slugify

class ChallengeApi(object):
	
	def __init__(self, id):
		self.id = id
		self.query_url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, self.id)
		self.challenge = self._get_datastore()
		self.data = None

		self._get_datastore():
		
	def _get_http(self):
		result = urlfetch.fetch(self.query_url)
		if result.status_code == 200:
			self._parse_data(result.content)
			return True
		else:
			self.id = 0
			return False
	
	def _get_datastore(self):
		return Challenge.query(Challenge.num == self.id).get()
	
	def resync(self):
		self._get_http()
		if self.challenge is None:
			return 'No challenge'
		if self._get_http():
			self.process_datapoints()
			
		return self.challenge
	
	def delete(self):
		self.url = self.challenge.url
		self.challenge.key.delete()
		
	def _insert_datastore(self):
		new_challenge = Challenge()
		new_challenge.num = self.id
		new_challenge.name = self.data['Name']
		new_challenge.type = self.data['Type']
		new_challenge.start = self.start
		new_challenge.end = self.end
		new_challenge.config = self.data['Configuration']
		for datapoint in self.data['DataPoints']:
			new_point = DataPoint()
			new_point.updated = datapoint['updated']
			new_point.value = datapoint['value']
			new_point.increment = datapoint['increment']
			new_challenge.datapoints.append(new_point)
		if self.url is not None:
			new_challenge.url = self.url
			
		new_challenge.put()
		self.challenge = new_challenge
	
	def _parse_data(self, content):
		self.data = json.loads(content)
		if type(self.data) is list and len(self.data) == 1:
			self.data = self.data[0]
		self._merge_data_config()
		
	def _merge_data_config(self):
		if self.data.has_key('Configuration']:
			self.data.update(data_dict)
			del self.data['Configuration']
	
	def get_start_date(self):
		return datetime.datetime.utcfromtimestamp(
			self.data['startdatetimeepoch']
		)
	
	def get_end_date(self):
		return self.start + config.DEFAULT_CHALLENGE_DURATION
		
	def get_type(self):
		if 'vs' in self.data['Name'] and self.data['Goal'] == 50:
			self.data['type'] = 'versus'
		else:
			self.data['type'] = 'counter'
	
	def process_datapoints(self):
		previous_value = 0.0
		
		for point in self.data['DataPoints']:
			new_point = DatePoint()
			time_human = point['DateTime']
			new_point.updated = datetime.datetime.strptime(
				time_human,
				config.STRIP_TIME_BASE
			) 
			new_point.updated -= config.API_DATETIME_ADJUST
			new_point.value = point['Value']
			new_point.increment = new_point.value - previous_value

			self.challenge.datapoints.append(new_point)
			previous_value = value
		self.challenge.put()
	
	def update_datapoints(self):
		self.challenge.datapoints 
		
	def __str__(self):
		if self.data is not None:
			return 'Challenge #%s - %s' % (self.id, self.data['Name'])
		else:
			return 'Invalid Challenge'