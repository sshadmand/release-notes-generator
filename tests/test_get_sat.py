from releasenotes import getsat_connect
import mock
from mock import patch
import logging
from mock import MagicMock
import settings

class TestGetSat:
    def test_clean_text(self):
        gscon = getsat_connect.GetSatConnect()
        cleaned_text = gscon._clean_text(" What's up G\" `  ")
        
        assert cleaned_text == "What's up G `"

    def test_slugify(self):
        gscon = getsat_connect.GetSatConnect()
        cleaned_text = gscon._slugify("LAPI v1.2")
        
        assert cleaned_text == "lapi-v12"

    def test_post_release_to_getsat_updates(self):
		gscon = getsat_connect.GetSatConnect()

		#data
		issues = [{"type": "bug", "id":"LWEB1", "summary": "Test bug"}]
		release_name = "Mock Test v1.0"
		anchor = "mock-test-v10"
		topic_id = 2700076
		update_text = "plain text"

		#mock call to post function
		gscon._create_getsat_update_text = MagicMock(return_value=update_text)
		gscon._post_to_getsat_topic = MagicMock(return_value={})
		gscon._slugify = MagicMock(return_value=anchor)

		#call main function
		response = gscon.post_release_to_getsat_updates(issues, release_name)
		
		#assertions
		gscon._create_getsat_update_text.assert_called_with(issues, release_name, anchor)
		gscon._post_to_getsat_topic.assert_called_with(update_text, topic_id)
		gscon._slugify.assert_called_with(release_name)

		assert response == "http://support.getsocialize.com/socialize/topics/socialize_release_updates_published_on_this_thread#%s" % anchor


    @patch('httplib.HTTPConnection')
    def test_getsat_connect(self, httpcon_mock):
        content = "content"
        topic_id = 333
        gscon = getsat_connect.GetSatConnect()

        #mocks        
        httpcon_mock.request = MagicMock()
        httpcon_mock.getresponse = MagicMock(return_value="response_text")

        #call main function
        gscon._post_to_getsat_topic(content, topic_id)

        #assertions
        httpcon_mock.request.assert_called_once()

    def test_create_getsat_update_text(self):
        issues = [{"type": "bug", "id":"LWEB1", "summary": "Test bug"}]
        release_name, anchor = "release_name", "anchor"
        gscon = getsat_connect.GetSatConnect()

        #mock
        gscon._clean_text = MagicMock(return_value="cleaned text")

        #call main function
        gscon._create_getsat_update_text(issues, release_name, anchor)

