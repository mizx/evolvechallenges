import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2
from packages import gviz_api

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import base

class ApiHandler(webapp2.RequestHandler):
    def get(self, id):
        if not id.isdigit():
            self.response.write('Invalid ID')
            self.error(500)
            return
        
        challenge = Challenge.query(Challenge.num == int(id)).get()
        description = {
            'updated': ('datetime', 'Updated'),
            'value': ('number', 'Value')
        }
        
        data = []
        for point in challenge.datapoints:
            data.append({
                'updated': point.updated,
                'value': point.increment
            })
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        json = data_table.ToJSon()
        self.response.write(json)
        

class ApiHandler_raw_json(webapp2.RequestHandler):
    def get(self, id):
        if not id.isdigit():
            self.response.write('Invalid ID')
            self.error(500)
            return
            
        challenge = Challenge.query(Challenge.num == int(id)).get()
        
        if challenge is None:
            self.response.write('None')
            self.error(404)
            return
        data = dict();
        cols = [{
            'label': 'Time',
            'type': 'datetime'
        }, {
            'label': 'Values',
            'type': 'number'
        }]
        data['increment'] = {
            'cols': cols,
            'rows': []
        }
        data['total'] = {
            'cols': cols,
            'rows': []
        }
        # formatting: https://developers.google.com/chart/interactive/docs/reference#dataparam
        # example: https://developers.google.com/chart/interactive/docs/php_example
        total = 0
        i = 0
        hours = 0
        counter = 0
        finished = 0
        for point in challenge.datapoints:
            if (i % 4) == 0:
                data['increment']['rows'].append({
                    'c': [
                        {'v': point.get_fdate_js(), 'f': 'test'},
                        {'v': counter}
                    ]
                })
                data['total']['rows'].append({
                    'c': [
                        {'v': hours},
                        {'v': total}
                    ]
                })
                counter = point.increment
                hours += 1
                finished = 1
            else:
                counter += point.increment
                finished = 0
            i += 1
            total += point.increment
        if not finished:
            data['increment']['rows'].append({
                'c': [
                    {'v': hours},
                    {'v': counter}
                ]
            })
            data['total']['rows'].append({
                'c': [
                    {'v': hours},
                    {'v': total}
                ]
            })
        self.response.write(json.dumps(data['increment']))