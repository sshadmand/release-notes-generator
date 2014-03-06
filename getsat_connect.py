
import httplib, urllib
import xml.dom.minidom
import settings
import base64
import re, os
import json 
import logging


class GetSatConnect():

    def __init__(self):
        username = settings.GETSAT_USERNAME
        password = settings.GETSAT_PASSWORD
        credentials = "%s:%s" % (username, password)
        credentials = base64.b64encode( credentials.encode() )
        credentials = credentials.decode("ascii")
        headers = {'Authorization': "Basic " + credentials, "Content-type": "application/json"}
        self.conn = httplib.HTTPConnection("api.getsatisfaction.com")

    def _post_to_getsat_topic(self, content, topic_id=2700076):
        payload = """{"reply": { "content" :"%s"}}""" % content

        uri = "/topics/%s/replies" % topic_id, data, headers
        conn.request("POST", uri)
        
        logging.info('GETSAT URI:' + uri)

        self.conn.request("GET", uri, payload, self.headers)

        response = self.conn.getresponse()
        data = response.read()
        data = json.loads(data)

        self.conn.close()
        return data

    def _clean_text(self, text):
        cleaned = text.strip().replace('"', "").encode("utf-8", 'replace')
        cleaned = ''.join(cleaned.split("\n"))
        return cleaned 

    def post_release_to_getsat_updates(self, issues):
        release_notes_plain = ""
        

        for issue in issues:
            release_notes_plain = "%s <p> [%s] %s - %s </p>" % ( release_notes_plain, issue["type"], issue["id"], issue["summary"])

        print self._clean_text(release_notes_plain)
                