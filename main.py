#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Copyright (c) 2011, Sean Shadmand

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

  * Neither the name of the the Beautiful Soup Consortium and All
    Night Kosher Bakery nor the names of its contributors may be
    used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, DAMMIT.
"""
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import httplib, urllib
import xml.dom.minidom
import settings
import base64
import re    

class PublishRelease(webapp.RequestHandler):
    def get(self):
        pass

    def post(self):
        get_sat_post = self.request.get("get_sat_post")       
        tweet = self.request.get("tweet")       
        response = send_getsat_post(get_sat_post) #, topic_id=3951187)
        send_tweet(tweet)



def clean_text(text):
    cleaned = text.strip().replace('"', "").encode("utf-8", 'replace')
    cleaned = ''.join(cleaned.split("\n"))
    return cleaned 

def get_project_options(app_id):
    socialize_opts = ""
    socialize_opts =  socialize_opts + """<option value="294005" %s >API</option>""" % ("selected" if app_id == "294005" else "")
    socialize_opts =  socialize_opts + """<option value="352393" %s>GS.Com Web</option>""" % ("selected" if app_id == "352393" else "")
    socialize_opts =  socialize_opts + """<option value="293827" %s>iOS SDK</option>""" % ("selected" if app_id == "293827" else "")
    socialize_opts =  socialize_opts + """<option value="293829" %s>Android</option>""" % ("selected" if app_id == "293829" else "")

    appmakr_opts = ""
    appmakr_opts =  appmakr_opts + """<option value="293825" %s>Android</option>""" % ("selected" if app_id == "293825" else "")
    appmakr_opts =  appmakr_opts + """<option value="293815" %s>iPhone</option>""" % ("selected" if app_id == "293815" else "")
    appmakr_opts =  appmakr_opts + """<option value="293831" %s>Qt</option>""" % ("selected" if app_id == "293831" else "")
    appmakr_opts =  appmakr_opts + """<option value="302467" %s>Web</option>""" % ("selected" if app_id == "302467" else "")
    appmakr_opts =  appmakr_opts + """<option value="293821" %s>Windows</option>""" % ("selected" if app_id == "293821" else "")
    return socialize_opts, appmakr_opts 
    

class DisplayStories(webapp.RequestHandler):

    def get(self):
        label = str(self.request.get("label"))
        post_release = self.request.get("post_release")
        app_id = str(self.request.get("app_id"))
        show_all = self.request.get("show_all")
        show_all_checkbox = "checked" if show_all else ""
        if not label:
            label = "v0."
        
        apps = {"294005":"API", "352393":"GS.Com Web", "293827":"iOS SDK", "293829":"Android SDK" }

        socialize_opts, appmakr_opts = get_project_options(app_id)

        self.response.out.write("""
                                <html>
                                <body onLoad="document.forms[0].label.focus()">
                                <form method="GET" action="">
                                 PT Project ID:
                                    <select name=app_id>
                                        <optgroup label="Socialize">
                                            %s
                                        </optgroup>                                        
                                        <optgroup label="AppMakr">
                                            %s                                           
                                        </optgroup>
                                    </select>
                                 Release Label: <input type=text name=label value="%s" tabindex=0>
                                 <input type="checkbox" name="show_all" id="show_all_checkbox"  %s> <label for="show_all_checkbox">Show All &nbsp;&nbsp;&nbsp;</label>
                                 <input type=submit>
                                 </form>
                                </body>
                                </html> 
                            """ % (socialize_opts, appmakr_opts, label, show_all_checkbox) )
        
        if app_id:
            uri = "/services/v3/projects/" + app_id + "/stories?filter=label%3A" + label + "%20includedone:true"
            params = urllib.urlencode({})
            headers = {"X-TrackerToken": settings.TRACKER_TOKEN}
            conn = httplib.HTTPConnection("www.pivotaltracker.com")
            conn.request("GET", uri, params, headers)
            response = conn.getresponse()
            status = response.status
            xml_response = response.read()
            dom = xml.dom.minidom.parseString(xml_response)
            stories = dom.getElementsByTagName("story")
            
            story_count = int(dom.getElementsByTagName("stories")[0].getAttribute("count"))
            
            html = ""
            release_status = "Sorry, no date for that search..."
            ready_for_release = True
            released_to_prod = True
            
            release_notes = ""
            release_notes_plain = ""
            if story_count > 0:
                release_notes = release_notes + "<ol id='copytext'>"
                for story in stories:
                  story_type = story.getElementsByTagName("story_type")[0].childNodes[0].data
                  current_state = story.getElementsByTagName("current_state")[0].childNodes[0].data  
              
                  if current_state != "accepted":
                      ready_for_release = False
                      if story_type == "release":
                          released_to_prod = False

                  labels = story.getElementsByTagName("labels")[0].childNodes[0].data
                  if show_all or (not story_type in ["release", "chore"] and not "private" in labels):
                    name = story.getElementsByTagName("name")[0].childNodes[0].data
                    url = story.getElementsByTagName("url")[0].childNodes[0].data                    
                    labels = labels.replace(",", " ").replace(label, "")
                    release_notes = release_notes + "<li><p>[%s] <a href='%s'>%s</a> [ %s]<p></li>" % ( story_type, url, name, labels)
                    release_notes_plain = release_notes_plain + "<p> [%s] %s [ %s]</p>" % ( story_type, name, labels)
                    
                release_notes = release_notes + "</ol>"
                html = html + release_notes
                
                
                if not show_all:
                    release_name = apps[app_id] + " " + label
                    release_name_slug = _slugify(apps[app_id] + " " + label)
                    bookmark = """<a name="%s"></a><br><br>""" % release_name_slug
                    release_notes_plain = bookmark + release_name + "<br><br>" + release_notes_plain
                    download = ""
                    if app_id == "293827" or app_id == "293829":
                        release_notes_plain = release_notes_plain + "<br><br>Download the latest SDK at http://www.getsocialize.com/sdk"
                        download = " get it at: https://github.com/socialize/socialize-sdk-android/downloads"
                        if app_id == "293827":
                            download = " get it at: https://github.com/socialize/socialize-sdk-ios/downloads"

                    get_sat_post = clean_text(release_notes_plain)
                    topic_url = "http://support.getsocialize.com/socialize/topics/socialize_release_updates_published_on_this_thread#%s" % release_name_slug
                    tweet = "Released %s! More details at: %s %s" % (release_name, topic_url, download)


                    html = html + """
                        <style>p.post a {font-size: 20px;text-decoration: none;}textarea {width:500px;height:100px;}p.norm {font-size:14px;} </style>
                        <h3>Ready to publish this release to the boards?</h3>
                        """

                    release_form = ""
                    release_form = release_form + """ <form method="POST" action"/publish_release" > """
                    release_form = release_form + """ <input type="hidden" name="app_id" value="%s" /><input type="hidden" name="label" value="%s" /> """ % (app_id, label)
                    release_form = release_form + """ <p class="norm">GetSat Post</p><textarea name="get_sat_post">%s</textarea>""" % get_sat_post
                    release_form = release_form + """ <p class="norm">Twitter Post</p><textarea name="tweet_post">%s</textarea> """ % tweet
                    release_form = release_form + """ <p class="norm"> <input type="submit" value="Post release to Twitter and GetSat" /></p> """
                    release_form = release_form + """ </form> """

                    html = html + release_form

                else: #NOT SHOW ALL
                    html = html + """<p>** <a href="?app_id=%s&label=%s">Uncheck "show all" to post release notes</a></p>""" % (app_id, label)
                
                
                if not ready_for_release:
                    release_status = "<h3 style='color:#900;'>Easy, tiger! This release is not ready for production yet...but it's in the cards.</h3>"
                elif released_to_prod:
                    release_status = "<h3>I think this release is already on production</h3>"
                else:
                    release_status = "<h3>Hmm...I see a release to prod in your future</h3>"

            
            html = release_status + html
            self.response.out.write(html)

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)    
    
def send_tweet(status):
    import tweepy
    consumer_key=settings.TWITTER_CONSUMER_KEY
    consumer_secret=settings.TWITTER_CONSUMER_SECRET
    access_token=settings.TWITTER_ACCESS_TOKEN
    access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(status)

def send_getsat_post(content, topic_id=2700076):
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

def create_release_todo(text, app_id):
   pass
    

def main():
    application = webapp.WSGIApplication([
                                        ('/', DisplayStories),
                                        ('/publish_release', PublishRelease),
                                            ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
