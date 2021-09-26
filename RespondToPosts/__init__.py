import logging
import time
import tweepy
import re
import datetime
import random
from ..utils import clean, get_api, is_content_offensive_or_invalid, get_generated_response, true_random_randint, true_random_choice
from .topics import cat_fact, other_topics
import pytz

import azure.functions as func

utc=pytz.UTC

def trim_reply(reply):
    return reply[:reply.rfind('.')+1] if len(reply) < 240 else trim_reply(reply[:reply.rfind('.')])


def get_random_trend(api):
    logging.info("Getting trend")
    trending = api.get_place_trends(23424977)  #USA

    def get_safe_trend(trending):
        trend = true_random_choice(trending[0]['trends'][:15])
        if not is_content_offensive_or_invalid(trend['name']):
            return trend['name']
        else:
            return get_random_trend(trending)

    return get_safe_trend(trending)


def get_tweets(api, topic):
    logging.info("Getting tweets for " + topic["search_term"] + '   ' + topic["result_type"])
    return api.search(q=topic["search_term"],
                      result_type=topic["result_type"],
                      count=100,
                      lang='en',
                      tweet_mode='extended')


def get_generated_prompt(api, prompts):
    retry_count = 0
    
    def get_prompt():
        nonlocal retry_count
        nonlocal api
        nonlocal prompts

        retry_count = retry_count + 1
        if retry_count > 10:
            raise Exception("Could not generate prompt text")

        try:
            shuffled_prompts = random.SystemRandom().sample(prompts, 5)
            promts_promt = "\n\n".join([x for x in shuffled_prompts])
            generated_prompt = get_generated_response(promts_promt, 300, temp=0.7)
            logging.info(generated_prompt)

            generated_prompt = generated_prompt.split('\n\n')[1]
            generated_prompt = clean(generated_prompt)

            logging.info(generated_prompt)

            if is_content_offensive_or_invalid(generated_prompt):
                logging.info("Offensive prompt content.")
                return get_prompt()
        
            if len(generated_prompt) < 10:
                logging.info("Prompt too short. " + generated_prompt)
                return get_prompt()

            if not any(x in generated_prompt.lower() for x in [
                "cat ", "cat ", "cats ", " cats" "cat.", "cats.", "cats'", "cat's", "kitten", "kitties", "kitty", "fact",
                "feline", "lion", "tiger", "cheetah", "machine learning", "artificial intelligence", " ai ", " a.i. ", "ai's", " ai."
            ]):
                logging.info("Prompt doesn't mention topic. " + generated_prompt)
                return get_prompt()

            return generated_prompt

        except:
            return get_prompt()
        
    return get_prompt()


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()
    trend = None
    
    topic = cat_fact

    def get_topic_tweets(api):
        nonlocal trend
        nonlocal topic

        tweets = get_tweets(api, topic)

        if len(tweets) <= 0:
            logging.info("None found. New topic.")
            topic = true_random_choice(other_topics)

            if topic == other_topics[0]:  #TRENDING
                trend = get_random_trend(api)
                topic["search_term"] = f'"{trend}" filter:safe -filter:links -filter:retweets'
                topic["include_term"] = trend
                if topic == other_topics[0] and trend and trend[0] == '#':
                    topic["hashtag"] = trend
                else:
                    topic["hashtag"] = ""

            tweets = get_tweets(api, topic)

        if len(tweets) > 0:
            return tweets
        else:
            logging.info("None found. New topic.")
            topic = true_random_choice(other_topics)
            return get_topic_tweets(api)

    tweet_reply_count = 0

    def tweet_reply(api):
        nonlocal topic
        nonlocal trend
        nonlocal tweet_reply_count

        tweet_reply_count = tweet_reply_count + 1
        if tweet_reply_count > 50:
            logging.info("Reply retry limit reached.")
            return
            
        tweets = get_topic_tweets(api)

        for tweet in tweets:
            recent_tweet = tweet.created_at > utc.localize((datetime.datetime.utcnow() -
                                               datetime.timedelta(minutes=44)))
            if not recent_tweet:
                continue
            
            if topic != cat_fact and not tweet.user.followers_count > 250:
                continue

            if topic == cat_fact and not any(x in tweet.full_text.lower()
                                             for x in topic["include_terms"]):
                logging.info("Missing include terms for cat fact.")
                logging.info(tweet.full_text.lower())
                continue

            cleantext = clean(tweet.full_text)

            if is_content_offensive_or_invalid(cleantext):
                logging.info("Offensive content.")
                continue
            if len(cleantext) < 50:
                logging.info("Too short.")
                continue
            if topic != other_topics[0] and not topic["include_term"].lower() in cleantext.lower():
                logging.info("Missing include terms after cleaning.")
                continue

            try:
                logging.info("Good tweet. Getting prompt.")

                prompt = get_generated_prompt(api, topic["prompts"])

                logging.info("Getting reply.")
                reply = get_generated_response(f"\"{cleantext}\". {prompt}", 280)

                reply = reply[:reply.rfind('.') + 1]
                if reply.count('.') > 2:
                    for _ in range(true_random_randint(0, reply.count('.') - 2)):
                        reply = reply[:reply.rfind('.') + 1]

                while reply.count(".") > 2 or len(reply) > 280:
                    reply = reply[:reply.rfind(".", 0, reply.rfind(".")) + 1]

                reply = f"{prompt} {reply}"

                reply = clean(reply)

                reply = trim_reply(reply)
                
                if len(reply) < 20:
                    logging.info("Too short.")
                    return tweet_reply(api)

                logging.info(reply)

                #look for garbage
                regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
                if regex.search(reply) == None and not is_content_offensive_or_invalid(reply):
                    logging.info("Good reply. Posting.")

                    logging.info("Posting.")
                    hashtag = topic["hashtag"]
                    
                    
                    logging.info("Liking tweet")
                    try:
                        api.create_favorite(tweet.id)
                    except:
                        return
                    logging.info("Liked.")

                    api.update_status(
                        f"{reply} {hashtag} https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    )

                    logging.info("Posted.")
                    return
                else:
                    logging.info("Bad characters.")

            except Exception as e:
                logging.info("Exception. " + str(e))
                return tweet_reply(api)

        logging.info("Tweets found, but none acceptable.")
        logging.info("New topic.")

        topic = true_random_choice(other_topics)
        logging.info(topic["search_term"])
        if topic == other_topics[0]:  #TRENDING
            trend = get_random_trend(api)
            topic["search_term"] = f'"{trend}" filter:safe -filter:links -filter:retweets'
            topic["include_term"] = trend
            if topic == other_topics[0] and trend and trend[0] == '#':
                topic["hashtag"] = trend
            else:
                topic["hashtag"] = ""

        return tweet_reply(api)

    tweet_reply(api)