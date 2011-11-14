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
        if not label:
            label = "v0."
        self.response.out.write("""
                                <html>
                                <body>
                                <form method="GET" action="">
                                PT Project ID:
                                    <select name=app_id>
                                        <optgroup label="Socialize">
                                            <option value="294005">API</option>
                                            <option value="352393">GS.Com Web</option>
                                            <option value="293827">iOS SDK</option>
                                            <option value="293829">Android SDK</option>
                                        </optgroup>                                        
                                        <optgroup label="AppMakr">
                                            <option value="293825">Android</option>
                                            <option value="293815">iPhone</option>
                                            <option value="293831">Qt</option>
                                            <option value="302467">Web</option>
                                            <option value="293821">Windows</option>                                            
                                        </optgroup>
                                    </select>
                                Release Label: <input type=text name=label value="%s">
                                <input type=submit>
                                </form>
                                </body>
                                </html>
                            """ % label)
        
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
                for story in stories:
                  story_type = story.getElementsByTagName("story_type")[0].childNodes[0].data
                  current_state = story.getElementsByTagName("current_state")[0].childNodes[0].data  
              
                  if current_state != "accepted":
                      ready_for_release = False
                      if story_type == "release":
                          released_to_prod = False
                      
                  if not story_type in ["release", "chore"]:
                    name = story.getElementsByTagName("name")[0].childNodes[0].data
                    url = story.getElementsByTagName("url")[0].childNodes[0].data
                    labels = story.getElementsByTagName("labels")[0].childNodes[0].data
                    labels = labels.replace(",", " ").replace(label, "")
                    html = html + "<p>[%s] <a href='%s'>%s</a> [ %s]<p>" % ( story_type, url, name, labels)
                
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
