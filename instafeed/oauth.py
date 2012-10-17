import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="FL6V9vrWlfVKzpFVB0iDmg"
consumer_secret="Td8Mn4BzStppzPNDblylAibTXmDfRt0gjzN1cFAI"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="865080817-IfvQRIRGIcgAhDuMMrZExYckK7I2AO5xf1EIJKX6"
access_token_secret="YfEFwpTG3VuzBGjzD6i7EKLPyxNpdA36RcNOVXnofM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print api.me().name

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's 
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps

api.update_status('Updating using OAuth authentication via Tweepy!') 
