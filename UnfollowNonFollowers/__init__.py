import logging
import time
from ..utils import get_api, true_random_randint, true_random_choice
import tweepy

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()

    followers = api.get_follower_ids('AICatFacts')
    friends = api.get_friend_ids('AICatFacts')

    unfollow_count = 0

    for friend in friends:

        if unfollow_count >= 10:
            break

        if friend not in followers and true_random_randint(0, 3) == 0:
            try:
                logging.info(f"Unfollowing {friend}")
                api.destroy_friendship(friend)
                unfollow_count = unfollow_count + 1
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break
