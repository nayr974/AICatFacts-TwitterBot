import logging
import time
import tweepy
from ..utils import get_api

import azure.functions as func


def followall(api):
    follow_count = 0;
    logging.info('Following followers.')
    for follower in tweepy.Cursor(api.followers).items():
        if follow_count >= 5:
            break

        if not follower.following:
            logging.info('Following ' + follower.screen_name)
            try:
                follow_count = follow_count + 1
                follower.follow()
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    followall(api)
