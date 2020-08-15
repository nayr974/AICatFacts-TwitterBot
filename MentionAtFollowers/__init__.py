import logging
import re
import datetime
import tweepy 
import time
from ..utils import clean, get_api, is_content_offensive, get_generated_response, true_random_randint, true_random_choice

import azure.functions as func

prompts = [
    'I\'m curious what FOLLOWER thinks about the fact that cats',
    'Hey FOLLOWER, my algorithms have computed that cats',
    'My AI is wondering what FOLLOWER thinks about the fact that cats',
    'My advanced AI thinks that FOLLOWER might find it interesting that cats',
    'My algorithms think that FOLLOWER might be interested in the fact that cats',
    'Can you please help FOLLOWER? My advanced AI doesn\'t understand why cats',
    'What does FOLLOWER think about the fact that cats', 'Hey FOLLOWER, I need some data to help me compute my next fact. Why do cats',
    'My advanced AI tells me that FOLLOWER\'s cat',
    'Your cat is very cute FOLLOWER. My algorithms tell me that it',
    'Hey FOLLOWER, does it make sense that my algorithms think that cats'
]

def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = get_api()
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers

#def main(req: func.HttpRequest) -> func.HttpResponse:
def main(mytimer: func.TimerRequest) -> None:
    number = true_random_randint(0, 100)
    if number != 1:
        logging.info(str(number) + " Doesn't feel right to post.")
        return

    api = get_api()
    followers = get_followers('AICatFacts')
    follower = true_random_choice(followers)
    logging.info(f'Tweeting at: {follower.screen_name}')

    prompt = true_random_choice(prompts)
    generate_count = 0

    def get_mention(prompt):

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 10:
            raise Exception('generation limit hit')

        try:
            logging.info("Getting mention")
            mention = get_generated_response(prompt, 200)
            mention = mention[:mention.find("\n")]
            mention = mention[:mention.rfind(".") + 1]
            mention = clean(prompt + ' ' + mention)
            logging.info(mention)

            if len(mention) < 8:
                return get_mention(prompt)

            if mention == prompt:
                return get_mention(prompt)

            regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
            if regex.search(mention) is not None or is_content_offensive(mention):
                return get_mention(prompt)

            return mention
        except:
            logging.info("Exception. Retrying.")
            return get_mention(prompt)

    mention = get_mention(prompt)
    logging.info("Posting mention.")
    api.update_status(f"{mention.replace('FOLLOWER', f'@{follower.screen_name}')} #cats")
