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
    
class DisplayStories(webapp.RequestHandler):
    def get(self):
        
        label = str(self.request.get("label"))
        app_id = str(self.request.get("app_id"))
        show_all = self.request.get("show_all")
        show_all_checkbox = "checked" if show_all else ""
        if not label:
            label = "v0."
            
        socialize_opts = ""
        socialize_opts =  socialize_opts + """<option value="294005" %s >API</option>""" % ("selected" if app_id == "294005" else "")
        socialize_opts =  socialize_opts + """<option value="352393" %s>GS.Com Web</option>""" % ("selected" if app_id == "352393" else "")
        socialize_opts =  socialize_opts + """<option value="293827" %s>iOS SDK</option>""" % ("selected" if app_id == "293827" else "")
        socialize_opts =  socialize_opts + """<option value="293829" %s>Android SDK</option>""" % ("selected" if app_id == "293829" else "")
                
        appmakr_opts = ""
        appmakr_opts =  appmakr_opts + """<option value="293825" %s>Android</option>""" % ("selected" if app_id == "293825" else "")
        appmakr_opts =  appmakr_opts + """<option value="293815" %s>iPhone</option>""" % ("selected" if app_id == "293815" else "")
        appmakr_opts =  appmakr_opts + """<option value="293831" %s>Qt</option>""" % ("selected" if app_id == "293831" else "")
        appmakr_opts =  appmakr_opts + """<option value="302467" %s>Web</option>""" % ("selected" if app_id == "302467" else "")
        appmakr_opts =  appmakr_opts + """<option value="293821" %s>Windows</option>""" % ("selected" if app_id == "293821" else "")
        
        
        
        
        

            
        self.response.out.write("""
                                <html>
                                <body>
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
                                Release Label: <input type=text name=label value="%s">
                                <input type="checkbox" name="show_all" %s> Show All &nbsp;&nbsp;&nbsp;
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
            
            if story_count > 0:
                html = html + "<ol id='copytext'>"
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
                    html = html + "<li><p>[%s] <a href='%s'>%s</a> [ %s]<p></li>" % ( story_type, url, name, labels)
                
                html = html + "</ol>"
                
                
                if not show_all:
                    html = html + """
                        <style>p.post a {font-size: 22px;text-decoration: none;}</style>
                        <h2>Ready to release?</a>
                        <p class="post">1. <a href="http://twitter.com/SocializeStatus" target="_blank">Announce release to SocializeStatus &raquo;</a></p>
                        <p class="post">2. <a href="http://support.getsocialize.com/socialize/topics/socialize_release_updates_published_on_this_thread#bottom" target="_blank">Publish release notes to GetSatisfaction &raquo;</a></p>
                    """
                else:
                    html = html + """<p>** <a href="?app_id=%s&label=%s">Uncheck "show all" to post release notes</a></p>""" % (app_id, label)
                
                
                if not ready_for_release:
                    release_status = "<h3 style='color:#900;'>Easy, tiger! This release is not ready for production yet...but it's in the cards.</h3>"
                elif released_to_prod:
                    release_status = "<h3>I think this release is already on production</h3>"
                else:
                    release_status = "<h3>Hmm...I see a release to prod in your future</h3>"

            
            html = release_status + html
            self.response.out.write(html)
        


def main():
    application = webapp.WSGIApplication([
                                        ('/', DisplayStories),
                                            ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
