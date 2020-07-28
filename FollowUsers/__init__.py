import logging
import time
import tweepy
from ..utils import get_api

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    logging.info('Searching hashtags')
    tweets = api.search(
        q=f'"#catsoftwitter" OR "machine learning" OR "artificial intelligence" filter:safe -filter:links -filter:retweets ',
        count=50,
        locale='en', 
        tweet_mode='extended')

    follow_count = 0

    for tweet in tweets:
        if follow_count >= 1:
            break

        if not any(
            x in tweet.full_text.lower() for x in [
                "#catsoftwitter ", "machine learning ", "artificial intelligence"
            ]):
            continue

        if not tweet.user.following and not "bot" in tweet.user.name.lower() and not "bot" in tweet.user.screen_name.lower() and not "bot" in tweet.user.description.lower():

            try:
                logging.info('Following ' + tweet.user.screen_name)
                follow_count = follow_count + 1
                api.create_friendship(screen_name=tweet.user.screen_name)
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break
