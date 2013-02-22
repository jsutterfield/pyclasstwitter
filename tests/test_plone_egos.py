import snack_underflow
import requests
import json

def test_even_batch():
    x = range(6)
    result = snack_underflow.batch_tweets(x, 3)
    assert(len(result) == 2)

def test_odd_batch():
    x = range(7)
    result = snack_underflow.batch_tweets(x, 3)
    assert(len(result) == 3)

def test_zero_batch():
    x = []
    result = snack_underflow.batch_tweets(x, 10)
    assert(len(result) == 0)

def test_one_batch():
    x = [1]
    result = snack_underflow.batch_tweets(x, 10)
    assert(len(result) == 1)

class MockRequestsData(object):
    def __init__(self, json_string):
        self.ojson = json_string
    def json(self):
        return json.loads(self.ojson)

def requests_get_mock(*args, **kwargs):
    x = """
    {"completed_in":0.028,"max_id":301104096029597697,"max_id_str":"301104096029597697","page":1,"query":"%23snackunderflow","refresh_url":"?since_id=301104096029597697&q=%23snackunderflow&include_entities=1","results":[{"created_at":"Mon, 11 Feb 2013 23:03:05 +0000","entities":{"hashtags":[{"text":"snackunderflow","indices":[10,25]}],"urls":[],"user_mentions":[{"screen_name":"bdbaddog","name":"William Deegan","id":14160875,"id_str":"14160875","indices":[0,9]}]},"from_user":"luke_brannon","from_user_id":42067923,"from_user_id_str":"42067923","from_user_name":"Luke Brannon","geo":null,"id":301104096029597697,"id_str":"301104096029597697","iso_language_code":"en","metadata":{"result_type":"recent"},"profile_image_url":"http:\/\/a0.twimg.com\/profile_images\/1093915717\/headshot_normal.png","profile_image_url_https":"https:\/\/si0.twimg.com\/profile_images\/1093915717\/headshot_normal.png","source":"&lt;a href=&quot;http:\/\/twitter.com\/download\/iphone&quot;&gt;Twitter for iPhone&lt;\/a&gt;","text":"@bdbaddog #snackunderflow got home and the girls mad me cupcakes!","to_user":"bdbaddog","to_user_id":14160875,"to_user_id_str":"14160875","to_user_name":"William Deegan","in_reply_to_status_id":300821805843746817,"in_reply_to_status_id_str":"300821805843746817"},{"created_at":"Mon, 11 Feb 2013 04:21:22 +0000","entities":{"hashtags":[{"text":"emeraldsprint","indices":[0,14]},{"text":"snackunderflow","indices":[15,30]}],"urls":[],"user_mentions":[],"media":[{"id":300821805847941121,"id_str":"300821805847941121","indices":[45,65],"media_url":"http:\/\/pbs.twimg.com\/media\/BCy71q5CEAEJzIW.jpg","media_url_https":"https:\/\/pbs.twimg.com\/media\/BCy71q5CEAEJzIW.jpg","url":"http:\/\/t.co\/ZlIFnVlS","display_url":"pic.twitter.com\/ZlIFnVlS","expanded_url":"http:\/\/twitter.com\/bdbaddog\/status\/300821805843746817\/photo\/1","type":"photo","sizes":{"orig":{"w":768,"h":1024,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"small":{"w":340,"h":453,"resize":"fit"},"medium":{"w":600,"h":800,"resize":"fit"},"large":{"w":768,"h":1024,"resize":"fit"}}}]},"from_user":"bdbaddog","from_user_id":14160875,"from_user_id_str":"14160875","from_user_name":"William Deegan","geo":null,"id":300821805843746817,"id_str":"300821805843746817","iso_language_code":"de","metadata":{"result_type":"recent"},"profile_image_url":"http:\/\/a0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","profile_image_url_https":"https:\/\/si0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","source":"&lt;a href=&quot;http:\/\/twitter.com\/download\/iphone&quot;&gt;Twitter for iPhone&lt;\/a&gt;","text":"#emeraldsprint #snackunderflow dinner starts http:\/\/t.co\/ZlIFnVlS","to_user":null,"to_user_id":0,"to_user_id_str":"0","to_user_name":null},{"created_at":"Mon, 11 Feb 2013 04:20:52 +0000","entities":{"hashtags":[{"text":"emeraldsprint","indices":[0,14]},{"text":"snackunderflow","indices":[15,30]}],"urls":[],"user_mentions":[],"media":[{"id":300821680023015424,"id_str":"300821680023015424","indices":[31,51],"media_url":"http:\/\/pbs.twimg.com\/media\/BCy7uWKCEAAt1Qz.jpg","media_url_https":"https:\/\/pbs.twimg.com\/media\/BCy7uWKCEAAt1Qz.jpg","url":"http:\/\/t.co\/M3SNj50u","display_url":"pic.twitter.com\/M3SNj50u","expanded_url":"http:\/\/twitter.com\/bdbaddog\/status\/300821680014626817\/photo\/1","type":"photo","sizes":{"orig":{"w":768,"h":1024,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"small":{"w":340,"h":453,"resize":"fit"},"medium":{"w":600,"h":800,"resize":"fit"},"large":{"w":768,"h":1024,"resize":"fit"}}}]},"from_user":"bdbaddog","from_user_id":14160875,"from_user_id_str":"14160875","from_user_name":"William Deegan","geo":null,"id":300821680014626817,"id_str":"300821680014626817","iso_language_code":"de","metadata":{"result_type":"recent"},"profile_image_url":"http:\/\/a0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","profile_image_url_https":"https:\/\/si0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","source":"&lt;a href=&quot;http:\/\/twitter.com\/download\/iphone&quot;&gt;Twitter for iPhone&lt;\/a&gt;","text":"#emeraldsprint #snackunderflow http:\/\/t.co\/M3SNj50u","to_user":null,"to_user_id":0,"to_user_id_str":"0","to_user_name":null},{"created_at":"Mon, 11 Feb 2013 04:20:15 +0000","entities":{"hashtags":[{"text":"emeraldsprint","indices":[0,14]},{"text":"snackunderflow","indices":[16,31]}],"urls":[],"user_mentions":[]},"from_user":"bdbaddog","from_user_id":14160875,"from_user_id_str":"14160875","from_user_name":"William Deegan","geo":null,"id":300821527501361152,"id_str":"300821527501361152","iso_language_code":"de","metadata":{"result_type":"recent"},"profile_image_url":"http:\/\/a0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","profile_image_url_https":"https:\/\/si0.twimg.com\/profile_images\/103716870\/me_pict_normal.jpg","source":"&lt;a href=&quot;http:\/\/twitter.com\/download\/iphone&quot;&gt;Twitter for iPhone&lt;\/a&gt;","text":"#emeraldsprint  #snackunderflow  start of dinner","to_user":null,"to_user_id":0,"to_user_id_str":"0","to_user_name":null}],"results_per_page":15,"since_id":0,"since_id_str":"0"}
    """
    return MockRequestsData(x)

def test_tweets_format():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert(len(result) == 4)

def test_tweets_sn():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('screen_name' in result[0])

def test_tweets_text():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('text' in result[0])

def test_tweets_sn():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('screen_name' in result[0])

def test_tweets_created_at():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('created_at' in result[0])

def test_tweets_profile_image():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('profile_image' in result[0])

def test_tweets_real_name():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('real_name' in result[0])

def test_tweets_media():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('media' in result[0])

def test_tweets_id():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert('id' in result[0])

def test_tweets_time_format():
    requests.get = requests_get_mock
    result = snack_underflow.get_tweets('emeraldsprint')
    assert(result[0]['create_at'] == '11 Feb -- 23:03:05')