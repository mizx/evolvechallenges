import config
from models import Challenge, DataPoint

import datetime
import logging
import json
import webapp2

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

def insert_previous_events():
    events = []
    
    # Val Predator Challenge
    event = Challenge()
    event.num = 6
    event.url = "http://evolvegame.com/news/val-predator-challenge-weekend"
    event.name = "Val Predator Challenge"
    event.type = 'counter'
    event.progress = 47722
    event.isComplete = True
    event.isAchieved = True
    event.goal = 35000
    event.goal_stretch = 45000
    event.start = datetime.datetime.strptime("2015-05-15 04:00:00", '%Y-%m-%d %H:%M:%S')
    event.end = start + config.DEFAULT_CHALLENGE_DURATION
    event.objective1_name = "Val Wins"
    events.append(event)
    
    # Lazarus vs. Kraken Challenge
    event = Challenge()
    event.num = 5
    event.url = 'http://evolvegame.com/news/evolves-lazarus-vs-kraken-challenge-weekend'
    event.name = 'Lazarus vs Kraken Challenge'
    event.type = 'versus'
    event.progress = 49.2
    event.isComplete = True
    event.isAchieved = True
    event.start = datetime.datetime.strptime("2015-05-08 04:00:00", '%Y-%m-%d %H:%M:%S')
    event.end = start + config.DEFAULT_CHALLENGE_DURATION
    event.objective1_name = "Lazarus Wins"
    event.objective2_name = "Kraken Wins"
    events.append(event)
    
    # Parnell Headshot Challenge
    event = Challenge()
    event.num = 4
    event.url = 'http://evolvegame.com/news/evolves-parnell-headshot-challenge-weekend'
    event.name = 'Parnell Headshot Challenge'
    event.type = 'counter'
    event.isComplete = True
    event.isAchieved = True
    event.goal = 2000000
    event.goal_stretch = 2800000
    event.start = datetime.datetime.strptime("2015-05-01 04:00:00", '%Y-%m-%d %H:%M:%S')
    event.end = start + config.DEFAULT_CHALLENGE_DURATION
    event.objective1_name = "Headshots"
    event.objective1_max = 2800000
    event.append(event)
    
    # Hyde vs. Wraith Throwdown Challenge
    event = Challenge()
    event.num = 3
    event.url = 'http://evolvegame.com/news/evolves-Hyde-vs-Wraith-throwdown-challenge-weekend'
    event.name = 'Hyde vs Wraith Throwdown Challenge'
    event.type = 'versus'
    event.progress = 46.23
    event.isComplete = True
    event.isAchieved = True
    event.start = datetime.datetime.strptime("2015-04-24 04:00:00", '%Y-%m-%d %H:%M:%S')
    event.end = start + config.DEFAULT_CHALLENGE_DURATION
    event.objective1_name = "Hyde Wins"
    event.objective2_name = "Wraith Wins"
    events.append(event)
    
    

class AdminHandler(webapp2.RequestHandler):
    def get(self, command=None):
        if command = 'addpreviousevents':
            insert_previous_events()

    def processData(self, results):
        return DataPoint.get_key
    
    
app = webapp2.WSGIApplication([
    (r'/admin/(\w+)?', AdminHandler)
], debug=True)