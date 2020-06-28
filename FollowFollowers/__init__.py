import logging
import time
import tweepy
from ..utils import get_api

import azure.functions as func


def followall(api):
    logging.info('Following all followers.')
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logging.info('Following ' + follower.screen_name)
            try:
                follower.follow()
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    followall(api)
