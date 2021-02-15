import urllib.request
import urllib.parse
import urllib.error
import ssl
import pprint
import requests
import twurl


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    print('')
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        break
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '20'})
    print('Retrieving', url)
    #connection = urllib.request.urlopen(url, context=ctx)
    #data = connection.read().decode()
    response = requests.get(url)
    print(response.status_code)
    #print(response.content)
    #print(response.headers)
    #print(response.text)
    data = response.json()
    pprint.pprint(data)
    #headers = dict(connection.getheaders())
    #print(headers)
    print('Remaining', response.headers['x-rate-limit-remaining'])
    #print('Remaining', headers['x-rate-limit-remaining'])
