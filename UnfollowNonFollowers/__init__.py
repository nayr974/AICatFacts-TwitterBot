import logging
import time
import random
from ..utils import get_api

import azure.functions as func

#def main(req: func.HttpRequest) -> func.HttpResponse:
def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    
    followers = api.followers_ids('AICatFacts')
    friends = api.friends_ids('AICatFacts')

    unfollow_count = 0
        
    for friend in friends:

        if unfollow_count >= 1:
            break

        if friend not in followers and random.SystemRandom().randint(0,3) == 0:
            try:
                logging.info(f"Unfollowing {friend}")
                api.destroy_friendship(friend)
                unfollow_count = unfollow_count + 1
                time.sleep(5)
            except tweepy.TweepError as e:
                #probably hit rate limit
                logging.info(e)
                break
                
