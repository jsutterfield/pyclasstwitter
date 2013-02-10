import requests
import urllib
from jinja2 import Environment, FileSystemLoader
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def send_hashtag_report(hashtag):
    tweets = get_tweets(hashtag)
    avatars, tweet_images = get_images(tweets)
    html = prepare_email(tweets)
    send_email("james.sutterfield@gmail.com", "smtp.gmail.com", 587, "nbpyclasstest@gmail.com", "EmereraldSprint", html,
               avatars, tweet_images)
    print "Success!"

def get_tweets(hashtag):
    print "Retrieving tweets..."
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
    t = env.get_template('email.html')
    html_email = t.render(tweets=tweets)
    return html_email

def send_email(addresses, host, port, from_address, subject, html_email,
               avatars, tweet_images):
    print "Sending email..."
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_address
    msgRoot['To'] = ', '.join(addresses)
    msgRoot.epilogue = ''

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('PLAIN TEXT GOES HERE')
    msgAlternative.attach(msgText)

    msgText = MIMEText(html_email.encode('utf-8'), 'html')
    msgAlternative.attach(msgText)

    for avatar in avatars:
        with open("{0}_av".format(avatar), 'rb') as fp:
            msgImage = MIMEImage(fp.read())
    for tweet_image in tweet_images:
        with open(tweet_image, 'rb') as fp:
            msgImage = MIMEImage(fp.read())
    
    for avatar in avatars:
        msgImage.add_header('Content-ID', '<{0}>_av'.format(avatar))
        msgRoot.attach(msgImage)
    for tweet_image in tweet_images:
        msgImage.add_header('Content-ID', tweet_image)
        msgRoot.attach(msgImage)

    session = smtplib.SMTP(host, port)
    session.starttls()
    session.login(from_address, "_passw0rd_")
    session.sendmail(from_address, addresses, msgRoot.as_string())
    session.quit()

if __name__ == '__main__':
    send_hashtag_report("emeraldsprint")