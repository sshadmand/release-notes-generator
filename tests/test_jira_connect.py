from releasenotes import jira_connect
import mock
from mock import patch
import logging
from mock import MagicMock
import settings

class TestJIRAConnect:

    @patch('httplib.HTTPConnection')
    def test_jira_jql(self, httpcon_mock):
        pass
        #mocks        
        
     #    httpcon_mock.request = MagicMock()
     #    httpcon_mock.getresponse = MagicMock(return_value="response_text")

    	# jira_con = jira_connect.JIRAConnect()
    	# jira_con.jira_jql()