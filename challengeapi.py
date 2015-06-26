import config
from models import DataPoint

import datetime
import logging
import json

from google.appengine.api import urlfetch

from django.template.defaultfilters import slugify

class ChallengeApi(object):
	
	def __init__(self, id):
		self.id = id
		self.query_url = '%s%s' % (config.URL_API_EVOLVE_CHALLENGE, self.id)
		self.data = None
		self._get_http()
		
	def _get_http(self):
		result = urlfetch.fetch(self.query_url)
		if result.status_code == 200:
			self._parse_data(result.content)
			logging.info('Successfully retrieved %s' % self)
			return True
		else:
			self.id = 0
			return False
	
	def _parse_data(self, content):
		self.data = json.loads(content)
		if type(self.data) is list and len(self.data) == 1:
			self.data = self.data[0]
		self._process_datapoints()
	
	def get_start_datetime(self):
		return datetime.datetime.utcfromtimestamp(
			self.data['Configuration']['StartDateTimeEpoch']
		)
	
	def get_end_datetime(self):
		return self.get_start_datetime() + config.DEFAULT_CHALLENGE_DURATION
	
	def get_name(self):
		return self.data['Name']
	
	def get_config(self):
		return self.data['Configuration']
	
	def get_slug(self):
		return slugify(self.get_name())
		
	def get_type(self):
		if 'vs' in self.data['Name'] and self.data['Goal'] == 50:
			return 'versus'
		else:
			return 'counter'

	def get_datapoints(self):
		return self.data['DataPoints']
			
	def _process_datapoints(self):
		previous_value = 0.0
		points = []
		
		start = self.get_start_datetime()
		end = self.get_end_datetime() + config.DEFAULT_CHALLENGE_POST_DELAY
		
		for point in self.data['DataPoints']:
			new_point = DataPoint()
			time_human = point['DateTime']
			new_point.updated = datetime.datetime.strptime(
				time_human,
				config.STRIP_TIME_BASE
			) 
			new_point.updated -= config.API_DATETIME_ADJUST
			if new_point.updated < start:
				continue
			if new_point.updated > end:
				continue
			new_point.value = point['Value']
			new_point.increment = new_point.value - previous_value

			points.append(new_point)
			previous_value = new_point.value
			
		self.data['DataPoints'] = points
		
	def __str__(self):
		if self.data is not None:
			return 'Challenge #%s - %s' % (self.id, self.data['Name'])
		else:
			return 'Invalid Challenge'