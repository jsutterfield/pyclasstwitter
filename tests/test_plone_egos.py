import plone_egos


def test_tweet():
    result = plone_egos.get_tweets("emeraldsprint")
    assert("twitter_id" in result.keys, "get_tweets is not finding key for twitter_id" )
