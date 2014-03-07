from releasenotes import twitter_connect
import mock
from mock import patch
import logging
from mock import MagicMock
import settings

class TestTwitterConnect:

    @patch('httplib.HTTPConnection')
    def test_send_tweet(self, httpcon_mock):
        pass
        #mocks        
        
     #    httpcon_mock.request = MagicMock()
     #    httpcon_mock.getresponse = MagicMock(return_value="response_text")

    	# jira_con = jira_connect.JIRAConnect()
    	# jira_con.jira_jql()