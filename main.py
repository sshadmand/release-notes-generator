import webapp2 as webapp
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import httplib, urllib
import xml.dom.minidom
import settings
import base64
import re, os
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from django.utils import simplejson 
import bitly
from jira_connect import *
import logging



class Index(webapp.RequestHandler):

    def post(self):
        pass
        
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, 
            {

            }
        ))


class GetIssues(webapp.RequestHandler):

    def post(self):
        return "{}"
        
    def get(self):
        jql = self.request.get("jql")
        logging.info('JQL Request:' + jql)
        jcon = jira_connect()
        data = jcon.jira_jql(search_string=jql)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

       

app = webapp.WSGIApplication([
                                        ('/', Index),
                                        ('/get_issues', GetIssues),

                                            ],
                                         debug=True)



if __name__ == '__main__':
    main()
