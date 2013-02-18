import requests
import urllib
from jinja2 import Environment, FileSystemLoader
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
import premailer
import os

def create_hashtag_html_pages(hashtag):
    tweets = get_tweets(hashtag)
    avatars, tweet_images = get_images(tweets)
    html_email, plain_email = prepare_email(tweets)
    delete_files(avatars, tweet_images)
    print "Success!"

def get_tweets(hashtag):
    print "Retrieving tweets..."
    tweet_list = []
    search_url = "http://search.twitter.com/search.json?q=%23{0}&include_entities=true".format(hashtag)
    next_page = True
    # Twitter api only serves 15 tweets per request. If json object has 'next_page' value keep
    # loading pages, otherwise stop
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
            each_tweet['created_at'] = tweet['created_at'][5:12] + '--' + tweet['created_at'][16:25]
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
    print "Downloading images..."
    avatars_downloaded = []
    tweet_images_downloaded = []
    for tweet in tweet_list:
        if tweet['screen_name'] not in avatars_downloaded:
            urllib.urlretrieve(tweet['profile_image'], '{0}_av'.format(tweet['screen_name']))
            avatars_downloaded.append(tweet['screen_name'])
        if tweet['media']:
            urllib.urlretrieve(tweet['media'], '{0}_im'.format(tweet['id']))
            tweet_images_downloaded.append('{0}_im'.format(tweet['id']))
    return avatars_downloaded, tweet_images_downloaded

def prepare_email(tweets):
    print "Preparing email..."
    env = Environment(loader=FileSystemLoader('templates'))
    html_template = env.get_template('simple-basic.html')
    plain_template = env.get_template('plaintext_email')
    html_email = html_template.render(tweets=tweets)
    plain_email = plain_template.render(tweets=tweets)
    # Converts all css stylings from those in the <head></head> into inline styling
    # so the email client doesn't rip them out.
    html_email = premailer.transform(html_email)
    return html_email, plain_email

def delete_files(avatars, tweet_images):
    print "Cleaing up directory..."
    dir_path = os.path.abspath(os.path.dirname(__file__))
    for avatar in avatars:
        os.remove(dir_path + "/" + "{0}_av".format(avatar))
    for tweet_image in tweet_images:
        os.remove(dir_path + "/" + tweet_image)

if __name__ == '__main__':
    create_hashtag_html_pages("emeraldsprint")
