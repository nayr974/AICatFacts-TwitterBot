import logging
import re
import datetime
import tweepy 
import time
import random
from ..utils import clean, get_api, is_content_offensive_or_invalid, get_generated_response, true_random_randint, true_random_choice

import azure.functions as func

prompts = [
    'I\'m curious what FOLLOWER thinks about the fact that cats',
    'Hey FOLLOWER, my algorithms have computed that cats',
    'My AI is wondering what FOLLOWER thinks about the fact that cats',
    'My advanced AI thinks that FOLLOWER might find it interesting that cats',
    'My algorithms think that FOLLOWER might be interested in the fact that cats',
    'Can you please help FOLLOWER? My advanced AI doesn\'t understand why cats',
    'What does FOLLOWER think about the fact that my algorithms say cats', 'Hey FOLLOWER, I need some data to help me compute my next fact. Why do cats',
    'My advanced AI tells me that FOLLOWER\'s cat',
    'Your cat is very cute FOLLOWER. My algorithms tell me that it',
    'Hey FOLLOWER, does it make sense that my algorithms think that cats',
    'My algorithms have computed that FOLLOWER''s cat',
    'My AI is gathering data. What does FOLLOWER think about the fact that cats',
]

def get_generated_prompt(api):
    retry_count = 0

    shuffled_prompts = random.SystemRandom().sample(prompts, 8)
    promts_promt = "\n\n".join([x for x in shuffled_prompts])
    
    def get_prompt():
        nonlocal retry_count
        nonlocal api

        retry_count = retry_count + 1
        if retry_count > 10:
            raise Exception("Could not generate prompt text")

        try:
            generated_prompt = get_generated_response(promts_promt, 220)
            generated_prompt = generated_prompt.split('\n\n')[1]
            generated_prompt = clean(generated_prompt)

            if is_content_offensive_or_invalid(generated_prompt):
                logging.info("Offensive prompt content." + generated_prompt)
                return get_prompt()
        
            if len(generated_prompt) < 10:
                logging.info("Prompt too short. " + generated_prompt)
                return get_prompt()
            
            if not any(x in generated_prompt.lower() for x in [
                " cat", "cat ", "cats ", " cats", "cat.", "cats.", "cats'", "cat's", "kitten", "kitties", "kitty",
                "feline", "lion", "tiger", "cheetah"
            ]):
                logging.info("Prompt doesn't mention cat. " + generated_prompt)
                return get_prompt()

            if not generated_prompt.count("FOLLOWER") == 1:
                logging.info("FOLLOWER occurance is not 1. " + generated_prompt)
                return get_prompt()

            return generated_prompt
        except:
            return get_prompt()

    prompt = get_prompt()
    logging.info(prompt)
    return prompt

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

def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    followers = get_followers('AICatFacts')
    follower = true_random_choice(followers)
    logging.info(f'Tweeting at: {follower.screen_name}')

    prompt = get_generated_prompt(api)
    generate_count = 0

    def get_mention(prompt):

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 10:
            raise Exception('generation limit hit')

        try:
            logging.info("Getting mention")
            mention = get_generated_response(prompt, 220)
            mention = mention[:mention.rfind(".") + 1]

            if len(mention) < 8:
                logging.info("Too short. " + mention)
                return get_mention(prompt)

            if "FOLLOWER" in mention:
                logging.info("Contains follower. " + mention)
                return get_mention(prompt)

            mention = clean(prompt + ' ' + mention)

            regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
            if regex.search(mention) is not None or is_content_offensive_or_invalid(mention):
                logging.info("Offensive.")
                return get_mention(prompt)

            return mention
        except:
            logging.info("Exception. Retrying.")
            return get_mention(prompt)

    mention = get_mention(prompt)
    logging.info("Posting mention.")
    logging.info(mention)
    api.update_status(f"{mention.replace('FOLLOWER', f'@{follower.screen_name}')} #cats")
