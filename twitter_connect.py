from twitter import *

class TwitterConnect():
	def __init__():
	    self.t = Twitter(
        			auth=OAuth(settings.TWITTER_OAUTH_TOKEN, settings.TWITTER_OAUTH_SECRET,
                    settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
		           )


	def _send_tweet(self, status):
    	r = t.statuses.update(status=status)
    	return r

    def tweet_release(self, release_name, more_info_url=None, download_url=None):
    	tweet = "Released %s!" % release_name
    	
    	if more_info_url:
    		tweet += "More details at: %s" % (topic_url)
    	if download_url:
    		tweet += " Download at: %s " % (download_url)

    	return self._send_tweet(status)