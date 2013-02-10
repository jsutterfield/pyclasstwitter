import twitter
import requests
import json
import urllib

def send_hashtag_report(hashtag, *email_to):
    tweets = get_tweets(hashtag)
    get_images(tweets)
    print tweets

def get_tweets(hashtag):
    api = twitter.Api()
    tweets = api.GetSearch(term = hashtag)
    tweet_list = []
    for tweet in tweets:
        each_tweet = {}
        each_tweet['text'] = tweet.text
        each_tweet['user_image'] = tweet.user.profile_image_url
        each_tweet['screen_name'] = tweet.user.screen_name
        each_tweet['id'] = tweet.id
        tweet_list.append(each_tweet)
    return tweet_list

def get_images(tweet_list):
    for etweet in tweet_list:
        stat_url = "https://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true" % etweet["id"]
        fp = requests.get(stat_url)
        js = json.loads(fp.text)
        etweet['media_url'] = None
        if "media" in js['entities']:
            if 'media_url' in js['entities']['media'][0]:
                etweet['media_url'] = True
                f = urllib.urlretrieve(js['entities']['media'][0]['media_url'], "image_%s.jpg" % etweet['id'])

def prepare_email(tweets):
    pass

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
send_hashtag_report('emeraldsprint')