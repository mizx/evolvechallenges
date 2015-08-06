import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2
from packages import gviz_api

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.api import memcache

import base

class ApiHandler(webapp2.RequestHandler):
	# change this to use slug
	def get(self, id):
		if not id.isdigit():
			if not id.startswith('-') and id[1:].isdigit():
				self.response.write('Invalid ID')
				self.error(500)
				return
		challenge = memcache.get('challenge_%s' % id)
		if challenge is None:
			challenge = Challenge.query(Challenge.num == int(id)).get()
			memcache.set('challenge_%s' % id, challenge, 60)
		description = {
			'updated': ('datetime', 'Time'),
			'value': ('number', challenge.config['YAxisLabel'])
		}
		
		data = []
		i = 0
		counter = 0
		values = []
		for point in challenge.datapoints:
			counter += point.increment
			values.append(point.value)
			if (i % 4) == 0:
				data.append({
					'updated': point.updated.replace(minute=0, second=0, microsecond=0),
					'value': counter if challenge.type == 'counter' else sum(values)/len(values)
				})
				counter = 0
				values = []
			i += 1
			
		data_table = gviz_api.DataTable(description)
		data_table.LoadData(data)
		json = data_table.ToJSon()
		self.response.write(json)
