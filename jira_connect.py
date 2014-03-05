
import httplib, urllib
import xml.dom.minidom
import settings
import base64
import re, os
import json 
import logging


class jira_connect():

    def __init__(self):
        username = settings.JIRA_USERNAME
        password = settings.JIRA_PASSWORD



        credentials = "%s:%s" % (username, password)
        credentials = base64.b64encode( credentials.encode() )
        credentials = credentials.decode("ascii")
        self.headers = {'Authorization': "Basic " + credentials, "Content-type": "application/json"}
        self.conn = httplib.HTTPSConnection("sharethis.atlassian.net")

    

    def jira_jql(self, search_string="Sprint=%22Sprint%20146%22%20and%20status=accepted"):
        payload=None
        uri = "/rest/api/2/search?username=sshadmand&jql=%s" % search_string
        
        logging.info('JQL URI:' + uri)

        self.conn.request("GET", uri, payload, self.headers)

        response = self.conn.getresponse()
        data = response.read()
        data = json.loads(data)


        self.conn.close()
        return data


# jcon = JIRA_connect()
# data = jcon.jira_jql()
# print data