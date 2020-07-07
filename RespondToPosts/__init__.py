import logging
import time
import tweepy
import re
import random
import datetime
from ..utils import clean, get_api, is_content_offensive, get_generated_response, set_random_seed
from .topics import topics

import azure.functions as func


def get_random_trend(api):
    logging.info("Getting trend")
    trending = api.trends_place(23424977)  #USA

    def get_safe_trend(trending):
        trend = random.choice(trending[0]['trends'][:15])
        if not is_content_offensive(trend['name']):
            return trend['name']
        else:
            return get_random_trend(trending)

    return get_safe_trend(trending)


#def main(req: func.HttpRequest) -> func.HttpResponse:
def main(mytimer: func.TimerRequest) -> None:
    set_random_seed()

    # Azure cron timers don't seem to allow schedules that go overnight (15-4), or have multiple timer triggers (15-24, 0-4)
    # so a code based check is used here instead.
    if datetime.datetime.utcnow().hour > 4 and datetime.datetime.utcnow().hour < 15:
        logging.info("Outside of run time range")
        return

    api = get_api()

    topic = random.choice(topics)
    trend = " "

    if topic == topics[0]:  #TRENDING
        trend = get_random_trend(api)
        topic["search_term"] = f'"{trend}" filter:safe -filter:links -filter:retweets'
        topic["include_term"] = trend        

    logging.info("Getting tweets for " + topic["search_term"] + '   ' + topic["result_type"])
    tweets = api.search(
        q=topic["search_term"], result_type=topic["result_type"], count=50, lang='en')
        
    for tweet in tweets:
        recent_tweet = tweet.created_at > (datetime.datetime.utcnow() - datetime.timedelta(hours=2))
        cleantext = clean(tweet.text)

        if recent_tweet and not is_content_offensive(cleantext) and len(cleantext) > 50:
            if topic != topics[0] and not topic["include_term"].lower() in cleantext.lower():
                continue
            try:
                logging.info("Good tweet. Getting reply.")
                prompt = random.choice(topic["prompts"])
                reply = clean(get_generated_response(f"\"{cleantext}\". {prompt}", 220))

                reply = reply[:reply.rfind('.') + 1]

                if len(reply) < 20:
                    continue

                if topic["include_first_sentance"] == True:
                    reply = f"{prompt} {reply}"

                reply = clean(reply)

                logging.info(reply)

                #look for garbage
                regex = re.compile('[@_#$%^&*()<>/\|}{~:]')
                if regex.search(reply) == None and not is_content_offensive(reply):
                    logging.info("Good reply. Posting. ")

                    if topic == topics[0] and trend[0] == '#':
                        reply = reply + f" {trend}"
                    
                    if (random.randint(1, 10) >= 9):
                        logging.info("Posting. ")
                        api.update_status(
                            f"{reply} https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                        )
                        logging.info("Posted. ")
                    else:
                        logging.info("Posting. ")
                        api.update_status(
                            f"@{tweet.user.screen_name} {reply}",
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True)
                        logging.info("Posted. ")
                    break
            except:
                continue
