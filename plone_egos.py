import argparse


def send_hashtag_report(hashtag, email_to):
    pass


def get_tweets(hashtag):
    pass


def get_image(image_url):
    pass


def prepare_email(tweets):
    pass


def send_email(content, addresses, host, port, to, from_address, subject,
               images):
    pass

if __name__ == '__main__':

    # Create Argparser
    parser = argparse.ArgumentParser(description="Sends and email report for \
                                    a specific hashtag")
    parser.add_argument("HASHTAG", help="The hashtag you want to run the \
                        report on")
    parser.add_argument('EMAIL', nargs='*', help="List of email addresses to \
                        #send too")

    cmdargs = parser.parse_args()

    send_hashtag_report(cmdargs.HASHTAG, cmdargs.EMAIL)
