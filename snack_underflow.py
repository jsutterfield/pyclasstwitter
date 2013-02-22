import requests
from jinja2 import Environment, FileSystemLoader
import os

def send_hashtag_report(hashtag, batch_size):
    tweets = get_tweets(hashtag)
    batched_tweets = batch_tweets(tweets, batch_size)
    prepare_html_pages(batched_tweets)
    print "html pages created"

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

def batch_tweets(tweets, batch_size):
    total_tweets = []
    for i in range(0, len(tweets), batch_size):
        total_tweets.append(tweets[i:i+batch_size])
    return total_tweets

def prepare_html_pages(tweets):
    print "Preparing html pages..."
    if not os.path.exists('www'):
        os.makedirs('www')
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')
    env = Environment(loader=FileSystemLoader('templates'))
    html_template = env.get_template('snack_underflow.html')
    for tweet in tweets:
        page_data = {}
        page_data['prev_page'] = False
        page_data['next_page'] = False
        page_data['current_page'] = tweets.index(tweet) + 1
        page_data['total_pages'] = len(tweets)
        if tweets.index(tweet) > 0:
            page_data['prev_page'] = True
        if tweets.index(tweet) < len(tweets) - 1:
            page_data['next_page'] = True
        html_page = html_template.render(tweets=tweet, page_data=page_data)
        file_name = '%s/snack_%s.html' % (save_dir, tweets.index(tweet) + 1)
        with open(file_name, 'w') as fp:
            fp.write(html_page.encode('utf-8'))

if __name__ == '__main__':
    send_hashtag_report("winning", 20)