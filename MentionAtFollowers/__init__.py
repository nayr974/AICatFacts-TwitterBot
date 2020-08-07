import logging
import re
import datetime
from ..utils import clean, get_api, is_content_offensive, get_generated_response, true_random_randint, true_random_choice

import azure.functions as func

prompts = [
    'I\'m curious what FOLLOWER thinks about the fact that cats',
    'Hey FOLLOWER, isn\'t it interesting that cats',
    'I\'m wondering what FOLLOWER thinks about the fact that cats',
    'I think FOLLOWER might find it interesting that cats',
    'My algorithms think that FOLLOWER might be interested in the fact that cats',
    'Can you please help FOLLOWER? My advanced AI doesn\'t understand why cats',
    'What does FOLLOWER think about the fact that cats', 'Hey FOLLOWER, Why do cats',
    'My advanced AI tells me that FOLLOWER\'s cat',
    'Your cat is very cute FOLLOWER. My algorithms tell me that it',
    'Hey FOLLOWER, does it make sense that my algorithms think that cats'
]


#def main(req: func.HttpRequest) -> func.HttpResponse:
def main(mytimer: func.TimerRequest) -> None:
    number = true_random_randint(0, 75)
    if number != 1:
        logging.info(str(number) + " Doesn't feel right to post.")
        return

    api = get_api()

    follower = true_random_choice(api.followers())
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
            mention = clean(mention)
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
    api.update_status(f"{prompt.replace('FOLLOWER', f'@{follower.screen_name}')} {mention} #cats")
