import requests
import urllib
import pprint
from jinja2 import Environment, FileSystemLoader
import os
import glob

TEMPLATE_DIR = '/home/snackunderflow/pyclasstwitter/templates'
WEB_DIR = '/home/snackunderflow/'

HTML_PAGE_STARTS_WITH = 'hashtag_page'
FILE_SUFFIX = '.html'

TWEETS_PER_PAGE = 10

# debug aid
def print_tweets_to_screen(tweets):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(tweets)

def print_tweets_to_file(tweets, file_name):
    with open(file_name, 'wb') as f:
        pp = pprint.PrettyPrinter(indent=2)
        f.write(pp.pformat(tweets))

# ---
# custom filters
def generate_file_name(num):
    if num == 1:
        return "index.html"
    else:
        return os.path.join(WEB_DIR, "{0}{1:03d}{2}".format(HTML_PAGE_STARTS_WITH,
            num, FILE_SUFFIX))

def resurrect_links(tweet_text, links):
    # links is a list of dict(s) containing info about links in the tweet
    if links:
        # if there are multiple links then sort in reverse order of indices
        if len(links) > 1:
            links.sort(key=lambda link:link['indices'], reverse=True)

        # resurrect each links, starting from the end of each tweet text moving
        # from right to left
        for link in links:
            start, end = link['indices']
            tweet_text = tweet_text[:start] + "<a href=\"" + link['resource_url'] + "\"" + ">" \
                + link['display_url'] + "</a>" + tweet_text[end:]
        return tweet_text

# ---
# main defs
def remove_files(directory, suffix):
    os.chdir(directory)
    files_to_remove = glob.glob("{0}{1}".format("*", suffix))
    for f in files_to_remove:
        os.remove(f)

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

            # list contains link info dicts
            each_tweet['links'] = []

            # add any media link, note that twitter only supports one media per tweet
            if 'media' in tweet['entities']:
                each_tweet['media_url'] = tweet['entities']['media'][0]['media_url']
                link = {}
                link['display_url'] = tweet['entities']['media'][0]['url']
                link['resource_url'] = tweet['entities']['media'][0]['media_url']
                link['indices'] = tweet['entities']['media'][0]['indices']
                each_tweet['links'].append(link)

            # add links from the url section
            if tweet['entities']['urls']:
                link = {}
                for url in tweet['entities']['urls']:
                    link['display_url'] = url['url']
                    link['resource_url'] = url['expanded_url']
                    link['indices'] = url['indices']
                    each_tweet['links'].append(link)

            # add tweet object to tweet list
            tweet_list.append(each_tweet)

        # next page
        if 'next_page' in tweets:
            search_url = "http://search.twitter.com/search.json{0}".format(tweets['next_page'])
        else:
            next_page = False

    return tweet_list

def split_tweets_into_pages(tweets, tweets_per_page):
    return [tweets[i:i+tweets_per_page] for i in range(0,
        len(tweets), tweets_per_page)]

def prepare_html_pages(tweets, tweets_per_page, directory):
    print "Generating html pages..."

    # tell jinja where to find the template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    # register custom filter
    env.filters['generate_file_name'] = generate_file_name
    env.filters['resurrect_links'] = resurrect_links
    html_template = env.get_template('simple-basic.html')

    # transform tweets list into list of lists
    # each sublist contains tweets_per_page number of tweets
    list_of_tweet_pages = split_tweets_into_pages(tweets, tweets_per_page)

    # generate file names, page links, and render pages
    # web pages starts with index 1 (e.g. hashtag_page001.html) so adjust
    # zero-based index accordingly

    # If no tweets, generate a generic index page
    if not list_of_tweet_pages:
        with open(os.path.join(TEMPLATE_DIR, "index.html"), 'rb') as in_file:
            with open (os.path.join(WEB_DIR, 'index.html'), 'wb') as out_file:
                out_file.write(in_file.read())
        return

    for num, page in enumerate(list_of_tweet_pages):
        page_file_name = generate_file_name(num+1)
        html_page = html_template.render(tweets=page, num_of_pages=len(list_of_tweet_pages),
            current_page=(num+1))

        # save to directory
        print "filename: %s" % ( page_file_name )
        with open(page_file_name, 'wb') as f:
            f.write(html_page.encode('utf-8'))

def create_hashtag_html_pages(hashtag):
    remove_files(WEB_DIR, FILE_SUFFIX)
    tweets = get_tweets(hashtag)

    prepare_html_pages(tweets, TWEETS_PER_PAGE, WEB_DIR)
    print "Success!"

if __name__ == '__main__':
    create_hashtag_html_pages("snackunderflow")
