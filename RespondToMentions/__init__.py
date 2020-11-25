import logging
import re
import datetime
from ..utils import clean, get_api, is_content_offensive, get_generated_response, true_random_randint, true_random_choice

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()

    logging.info("Getting mentions")
    mentions = api.mentions_timeline(count=3, tweet_mode='extended')

    for tweet in mentions:
        recent_tweet = tweet.created_at > (datetime.datetime.utcnow() -
                                           datetime.timedelta(minutes=5))
        if recent_tweet:

            cleantext = clean(tweet.full_text)
            if not is_content_offensive(cleantext):
                logging.info('Good mention. Replying to: ' + cleantext)

                generate_count = 0

                def get_reply(cleantext):

                    nonlocal generate_count
                    generate_count = generate_count + 1
                    if generate_count > 20:
                        raise Exception('generation limit hit')

                    prompt = f'I am a machine learned artificial intelligence that talks about cats a lot. You said "{cleantext} Meow." Being a cute cat robot my algorithm replied, "'

                    try:
                        reply = get_generated_response(prompt, 200)
                        logging.info(reply)
                        reply = reply[:reply.find('"') + 1]
                        reply = clean(reply)
                        logging.info(reply)

                        if len(reply) < 8:
                            return get_reply(cleantext)

                        if reply == cleantext:
                            return get_reply(cleantext)

                        if reply == prompt:
                            return get_reply(cleantext)

                        regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
                        if regex.search(reply) is not None or is_content_offensive(reply):
                            return get_reply(cleantext)

                        return reply
                    except:
                        return get_reply(cleantext)

                reply = get_reply(cleantext)
                logging.info("Posting reply.")

                #If not a reply to another tweet, retweet with comment otherwise reply
                if tweet.in_reply_to_status_id is None:
                    api.update_status(
                        f"{reply} @{tweet.user.screen_name} https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    )
                else:
                    api.update_status(f"@{tweet.user.screen_name} {reply}",
                                      in_reply_to_status_id=tweet.id,
                                      auto_populate_reply_metadata=True)
                logging.info("Liking tweet")
                api.create_favorite(tweet.id)
                logging.info("Liked.")
