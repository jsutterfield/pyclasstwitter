import requests
import urllib
import pprint
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = '/Users/phong/PyClass/feb17_hashtag/templates'
WEB_DIR = '/Users/phong/PyClass/feb17_hashtag/www'

HTML_PAGE_STARTS_WITH = 'hashtag_page'
FILE_SUFFIX = '.html'

TWEETS_PER_PAGE = 10

# custom filter
def generate_file_name(num):
    return os.path.join(WEB_DIR, "{0}{1:03d}{2}".format(HTML_PAGE_STARTS_WITH,
        num, FILE_SUFFIX))

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

        # debug aid
        #pp = pprint.PrettyPrinter(indent=2)
        #pp.pprint(tweets)

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
            each_tweet['urls'] = False

            # add any media links
            if 'media' in tweet['entities']:
                each_tweet['media'] = tweet['entities']['media'][0]['media_url']

            # add any url
            if tweet['entities']['urls']:
                # list of urls, each url is a dict
                each_tweet['urls'] = tweet['entities']['urls']

            # add tweet object to tweet list
            tweet_list.append(each_tweet)

        # next page
        if 'next_page' in tweets:
            search_url = "http://search.twitter.com/search.json{0}".format(tweets['next_page'])
        else:
            next_page = False

    return tweet_list

def prepare_html_pages(tweets, tweets_per_page, directory):
    print "Generating html pages..."

    # tell jinja where to find the template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    # register custom filter
    env.filters['generate_file_name'] = generate_file_name
    html_template = env.get_template('simple-basic.html')

    # transform tweets list into list of lists
    # each sublist contains tweets_per_page number of tweets
    list_of_tweet_pages = [tweets[i:i+tweets_per_page] for i in range(0,
        len(tweets), tweets_per_page)]

    # generate file names, page links, and render pages
    # web pages starts with index 1 (e.g. hashtag_page001.html) so adjust
    # zero-based index accordingly
    for num, page in enumerate(list_of_tweet_pages):
        # html pages start with hashtag_page000.html
        page_file_name = generate_file_name(num+1)
        html_page = html_template.render(tweets=page, num_of_pages=len(list_of_tweet_pages),
            current_page=(num+1))

        # save to directory
        print "filename: %s" % ( page_file_name )
        with open(page_file_name, 'wb') as f:
            f.write(html_page.encode('utf-8'))

def create_hashtag_html_pages(hashtag):
    tweets = get_tweets(hashtag)
    print "retrieved %d tweets. " % ( len(tweets) )

    prepare_html_pages(tweets, TWEETS_PER_PAGE, WEB_DIR)
    print "Success!"


if __name__ == '__main__':
    create_hashtag_html_pages("brompton")
