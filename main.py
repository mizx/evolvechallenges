import config
import models
import pprint

import cgi
import urllib
import webapp2
import challengeapi

from google.appengine.ext import ndb

class MainHandler(webapp2.RequestHandler):
    def get(self):
        c = challengeapi.ChallengeApi(7)
        output = pprint.pprint(c.get_data())
        self.response.out.write(output)
        #self.response.out.write(c.Name)
        return
        query = models.Challenge.query().order(-models.Challenge.num)
        result = query.fetch(1)
        template_vars = {}
        if len(result):
            template_vars['challenge'] = result[0]
        template = config.JINJA_ENV.get_template('index.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
