import logging
import time
import tweepy
from ..utils import get_api

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    logging.info('Searching hashtags')
    tweets = api.search(
        q=f'"#catsoftwitter" -filter:links',
        count=10,
        locale='en')
    for tweet in tweets:
        if not tweet.user.following:
            try:
                logging.info('Following ' + tweet.user.screen_name)
                api.create_friendship(screen_name=tweet.user.screen_name)
                time.sleep(5)
            except tweepy.TweepError as e:
                logging.info(e)
