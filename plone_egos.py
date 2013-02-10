import twitter
import requests
import json
import urllib

def send_hashtag_report(hashtag, *email_to):
    pass


def get_tweets(hashtag):
    api = twitter.Api()
    #tweets = api.GetSearch(term = hashtag)
    search = "http://search.twitter.com/search.json?q=%23emeraldsprint&src=typd"
    fp = requests.get(search)
    import pdb; pdb.set_trace()
    tweets = fp.json()
    tweet_list = []
    for tweet in tweets:
        each_tweet = {}
        each_tweet['text'] = tweet.text
        each_tweet['user_image'] = tweet.user.profile_image_url
        each_tweet['screen_name'] = tweet.user.screen_name
        each_tweet['id'] = tweet.id
        tweet_list.append(each_tweet)
    return tweet_list

def get_image(tweet_list):
    for etweet in tweet_list:
        stat_url = "https://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true" % etweet["id"]
        fp = requests.get(stat_url)
        js = json.loads(fp.text)
        etweet['media_url'] = None
        if "media" in js['entities']:
            if 'media_url' in js['entities']['media'][0]:
                etweet['media_url'] = True
                f = urllib.urlretrieve(js['entities']['media'][0]['media_url'], "image_%s" % etweet['id'])



def prepare_email(tweets):
    pass

#def send_email(content, addresses, host, port, to, from, subject, images):
    #pass

#if __name__ == 'main':
    #send_hashtag_report()
l = get_tweets("emeraldsprint")
get_image(l)
print l