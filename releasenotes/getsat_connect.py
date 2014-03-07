
import httplib, urllib
import xml.dom.minidom
import settings
import base64
import re, os
import json 
import logging


class GetSatConnect():

    def __init__(self):
        pass

    #Need to clean this up and seperate out auth from post etc
    def _post_to_getsat_topic(self, content, topic_id):
        username = settings.GETSAT_USERNAME
        password = settings.GETSAT_PASSWORD
        
        credentials = "%s:%s" % (username, password)
        credentials = base64.b64encode( credentials.encode() )
        credentials = credentials.decode("ascii")
        headers = {'Authorization': "Basic " + credentials, "Content-type": "application/json"}

        data = """{"reply": { "content" :"%s"}}""" % content

        conn = httplib.HTTPConnection("api.getsatisfaction.com")
        conn.request("POST", "/topics/%s/replies" % topic_id, data, headers)
        response = conn.getresponse()

        data = response.read()
        conn.close()

        return data

    def _clean_text(self, text):
        cleaned = text.strip().replace('"', "").encode("utf-8", 'replace')
        cleaned = ''.join(cleaned.split("\n"))
        return cleaned 

    def _slugify(self, value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        import unicodedata
        _slugify_strip_re = re.compile(r'[^\w\s-]')
        _slugify_hyphenate_re = re.compile(r'[-\s]+')
        
        if not isinstance(value, unicode):
            value = unicode(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(_slugify_strip_re.sub('', value).strip().lower())
        return _slugify_hyphenate_re.sub('-', value)

    def _create_getsat_update_text(issues, release_name, anchor):
        release_notes_plain = "<a name='%s'></a><p>%s:</p>" % (anchor, release_name)

        for issue in issues:
            release_notes_plain = "%s <p> [%s] %s - %s </p>" % ( release_notes_plain, issue["type"], issue["id"], issue["summary"])

        release_notes_plain = self._clean_text(release_notes_plain)

        return release_notes_plain

    def post_release_to_getsat_updates(self, issues, release_name):
        topic_id = 2700076
        anchor = self._slugify(release_name)
        release_notes = self._create_getsat_update_text(issues, release_name, anchor)
        response = self._post_to_getsat_topic(release_notes, topic_id)

        return "http://support.getsocialize.com/socialize/topics/socialize_release_updates_published_on_this_thread#%s" % anchor



