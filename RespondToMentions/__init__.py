import logging
import re
import random
import datetime
from ..utils import clean, get_api, is_content_offensive, get_generated_response

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    api = get_api()

    logging.info("Getting mentions")
    mentions = api.mentions_timeline(count=20)

    for tweet in mentions:
        recent_tweet = tweet.created_at > (
            datetime.datetime.utcnow() - datetime.timedelta(minutes=30))
        if recent_tweet:

            #If a reply to another tweet, only a chance we will reply again
            if tweet.in_reply_to_status_id is not None:
                if random.SystemRandom().randint(0, 1) == 0:
                    continue

            logging.info('Replying to: ' + tweet.text)
            cleantext = clean(tweet.text)
            if not is_content_offensive(cleantext):
                logging.info("Good mention. Getting reply.")

                generate_count = 0

                def get_reply(cleantext):

                    nonlocal generate_count
                    generate_count = generate_count + 1
                    if generate_count > 20:
                        raise Exception('generation limit hit')

                    prompt = f'I am a machine learned artificial intelligence that talks about cats a lot. You said, "{cleantext}" Being a cat, I said "'

                    reply = get_generated_response(f"\"{cleantext}\". {prompt}", 160)
                    reply = reply[:reply.find('"')]
                    reply = clean(reply)
                    reply = reply[:reply.find('.')]

                    if len(reply) < 8:
                        return get_reply(cleantext)

                    if reply == cleantext:
                        return get_reply(cleantext)

                    regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
                    if regex.search(reply) is not None and not is_content_offensive(reply):
                        return get_reply(cleantext)

                    return reply

                reply = get_reply(cleantext)
                logging.info("Posting reply.")
                    
                #If not a reply to another tweet, retweet with comment otherwise reply
                if tweet.in_reply_to_status_id is None:
                    api.update_status(
                        f"@{tweet.user.screen_name} {reply} https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                    )
                else:
                    api.update_status(
                        f"@{tweet.user.screen_name} {reply}",
                        in_reply_to_status_id=tweet.id,
                        auto_populate_reply_metadata=True)
