import config
from google.appengine.ext import ndb

def challenge_key(challenge_name=config.DEFAULT_CHALLENGE_KEY):
    return ndb.Key('Challenge', challenge_name)

class Challenge(ndb.Model):
    num = ndb.IntegerProperty()
    url = ndb.TextProperty()
    name = ndb.StringProperty()
    type = ndb.StringProperty(choices=['counter', 'versus'], default='counter')
    progress1 = ndb.FloatProperty(default=0)
    isComplete = ndb.BooleanProperty(default=False)
    isAchieved = ndb.BooleanProperty(default=False)
    goal = ndb.IntegerProperty(default=None)
    goal_stretch = ndb.IntegerProperty(default=None)
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    objective1_name = ndb.StringProperty()
    objective1_max = ndb.IntegerProperty()
    objective1_min = ndb.IntegerProperty(default=0)
    objective2_name = ndb.StringProperty()
    objective2_max = ndb.IntegerProperty()
    objective2_min = ndb.IntegerProperty()
    
    @classmethod
    def get_name(self):
        return challenge_key()
    
    @classmethod
    def get_config_keys():
        return ['goal', 'start', 'end', 'objective',
                'objective_max', 'objective_min']

class DataPoint(ndb.Model):
    challengeId = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty()
    value = ndb.FloatProperty()
    increment = ndb.FloatProperty()