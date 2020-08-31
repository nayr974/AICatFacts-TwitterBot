import logging
import time
import tweepy
from ..utils import get_api, is_content_offensive

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()

    logging.info("Search terms")
    tweets = api.search(
        q=
        f'"artificial intelligence" OR "cute cat" OR "adorable cat" OR "machine learning" OR "cat fact" OR "#catsoftwitter" filter:safe -filter:links -filter:retweets',
        lang='en',
        result_type="recent",
        count=3,
        tweet_mode='extended')
    for tweet in tweets:
        if tweet.favorited == False and not is_content_offensive(tweet.full_text):
            try:
                logging.info("Fav!")
                api.create_favorite(tweet.id)
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break
