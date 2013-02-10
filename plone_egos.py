import twitter
import requests
import json
import urllib
from jinja2 import Environment, FileSystemLoader
import os

def send_hashtag_report(hashtag, *email_to):
    tweets_list = get_tweets(hashtag)
    tweets_list_images = get_images(tweets_list)
    prepare_email(tweets_list_images)

def get_tweets(hashtag):
    tweet_list = []
    search_url = "http://search.twitter.com/search.json?q=%23{0}&include_entities=true".format(hashtag)
    next_page = True
    while next_page:
        fp = requests.get(search_url)
        tweets = fp.json()
        for tweet in tweets['results']:
            if tweet['text'][:2] == 'RT':
                continue
            each_tweet = {}
            each_tweet['text'] = tweet['text']
            each_tweet['screen_name'] = tweet['from_user']
            each_tweet['real_name'] = tweet['from_user_name']
            each_tweet['profile_image'] = tweet['profile_image_url']
            each_tweet['id'] = tweet['id']
            each_tweet['created_at'] = tweet['created_at']
            each_tweet['media'] = False
            if 'media' in tweet['entities']:
                each_tweet['media'] = tweet['entities']['media'][0]['media_url']
            tweet_list.append(each_tweet)
        if 'next_page' in tweets:
            search_url = "http://search.twitter.com/search.json{0}".format(tweets['next_page'])
        else:
            next_page = False
    return tweet_list

def get_images(tweet_list):
    avatars_downloaded = []
    for tweet in tweet_list:
        if tweet['screen_name'] not in avatars_downloaded:
            urllib.urlretrieve(tweet['profile_image'], '{0}'.format(tweet['screen_name']))
            avatars_downloaded.append(tweet['screen_name'])
        if tweet['media']:
            urllib.urlretrieve(tweet['media'], '{0}'.format(tweet['id']))

def prepare_email(tweets):
    env = Environment(loader=FileSystemLoader('templates'))
    t = env.get_template('email.html')
    html_email = t.render(tweets=tweets)
    file_location = os.path.abspath(os.path.dirname(__file__))
    with open("{0}/templates/email2.html".format(file_location), 'w') as email:
        email.write(html_email.encode('utf-8'))

def send_email(addresses, host, port, from_address, subject):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_address
    msgRoot['To'] = ', '.join(addresses)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('PLAIN TEXT GOES HERE')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('image1.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    session = smtplib.SMTP(host, port)
    session.starttls()
    session.login(from_address, "_passw0rd_")
    session.sendmail(from_address, addresses, msgRoot.as_string())
    session.quit()



#if __name__ == 'main':
    #send_hashtag_report()
# l = get_tweets("emeraldsprint")
# get_image(l)
# print l
l = get_tweets('emeraldsprint')
prepare_email(l)