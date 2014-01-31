import urllib
import settings
from django.utils import simplejson 

def shorten(url):

    cleaned_url = urllib.quote(url)

    bitly_url = "http://api.bit.ly/shorten?version=2.0.1&longUrl=%s&login=getsocialize&apiKey=%s" % (cleaned_url, settings.BITLY_API_KEY) 
    
    f = urllib.urlopen(bitly_url)
    jsonit = f.read()
    f.close()

    data = simplejson.loads(jsonit)
    return data["results"][url]["shortUrl"]

