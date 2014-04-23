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
from releasenotes.jira_connect import *
from releasenotes.getsat_connect import *
from releasenotes.twitter_connect import *
import logging

from google.appengine.api import users

class Index(webapp.RequestHandler):

    def post(self):
        pass
        
    def get(self):

        user = users.get_current_user()

        if user and "@sharethis.com" in user.email():
            logging.info( "LOGGED IN AS: %s" %  user.email() ) 
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, 
                {
                    "logout_url": users.create_logout_url("/login"),
                    "user": user.email()
                }
            ))
        else:
            logging.info(  "NOT LOGGED IN" )
            self.redirect("/login")

class Login(webapp.RequestHandler):

    def post(self):
        pass
        
    def get(self):

        user = users.get_current_user()

        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url("/login")
        
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        self.response.out.write(template.render(path, 
            {
                "user": user,
                "page": "login",
                "logout_url": logout_url,
                "login_url": login_url,
            }
        ))
         


class GetIssues(webapp.RequestHandler):

    def post(self):
        return None
        
    def get(self):
        jql = self.request.get("jql")
        logging.info('JQL Request:' + jql)

        jcon = JIRAConnect()
        data = jcon.jira_jql(search_string=jql)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))

class PostIssuesToTwitterAndGetSat(webapp.RequestHandler):

    def post(self):
        issues = self.request.get("issues")
        issues = json.loads(issues)

        release_name = self.request.get("release_name")

        #post notes to GetSat thread
        getsat_conn = GetSatConnect()
        more_info_url = getsat_conn.post_release_to_getsat_updates(issues, release_name)

        download_url = None
        if "SAND" in release_name or "SIOS" in release_name:
            download_url = "http://www.getsocialize.com/sdk"

        #post release to SocializeStatus Twitter thread
        twit_conn = TwitterConnect();
        twit_conn.tweet_release(release_name, more_info_url, download_url);

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write("{}")
        
    def get(self):
        return None        


app = webapp.WSGIApplication([
                                        ('/', Index),
                                        ('/login', Login),
                                        ('/get_issues', GetIssues),
                                        ('/post_issues_to_twitter_and_getsat', PostIssuesToTwitterAndGetSat),

                                            ],
                                         debug=True)



if __name__ == '__main__':
    main()
