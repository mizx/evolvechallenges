import json
import webapp2
import tools

import model

class JsonBaseHandler(webapp2.RequestHandler):

  def send_json(self, data):
    self.response.headers['content-type'] = 'application/json'
    self.response.write(json.dumps(data, default=tools.json_date_handler))
    

class ChallengesHandler(JsonBaseHandler):

  def get(self):
    challenges = model.AllChallenges()
    data = [challenge.to_dict() for challenge in challenges]
    self.send_json(data)

"""
class UpdateHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.UpdateGuest(r['id'], r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class InsertHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.InsertGuest(r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class DeleteHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    model.DeleteGuest(r['id'])
"""

app = webapp2.WSGIApplication([
    ('/api/challenges', ChallengesHandler),
], debug=True)


