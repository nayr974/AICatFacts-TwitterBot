import logging
import time
import tweepy
from ..utils import get_api

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    logging.info('Searching hashtags')
    tweets = api.search(
        q=f'"#catsoftwitter" filter:safe -filter:links -filter:retweets ',
        count=3,
        locale='en')
    for tweet in tweets:
        if not tweet.user.following:
            try:
                logging.info('Following ' + tweet.user.screen_name)
                api.create_friendship(screen_name=tweet.user.screen_name)
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break
