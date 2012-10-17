import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="FL6V9vrWlfVKzpFVB0iDmg"
consumer_secret="Td8Mn4BzStppzPNDblylAibTXmDfRt0gjzN1cFAI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

print redirect_url

session.set('request_token', (auth.request_token.key, auth.request_token.secret))

verifier = raw_input('Verifier:')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
token = session.get('request_token')
session.delete('request_token')
auth.set_request_token(token[0], token[1])

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print 'Error! Failed to get access token.'

api = tweepy.API(auth)
api.update_status('tweepy + oauth!')
