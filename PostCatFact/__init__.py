import logging
import re
import time

from datetime import datetime
from ..utils import clean, get_api, get_generated_catfact, upload_cat_image, true_random_randint, true_random_choice, is_content_offensive_or_invalid
from ..catfacts import facts

import azure.functions as func


def get_seed_facts():
    split_facts = facts.split("\n")
    seed_facts = [
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts),
        true_random_choice(split_facts)
    ]
    return "\n\n".join(seed_facts) + "\n\nHere's an interesting fact about cats."


def main(mytimer: func.TimerRequest) -> None:

    generate_count = 0

    def generate_fact():

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 30:
            raise Exception('generation limit hit')

        logging.info('Generating fact.')

        try:
            fact = get_generated_catfact(get_seed_facts())
        except Exception as e:
            logging.info('Exception.' + str(e))
            time.sleep(15)
            return generate_fact()

        if fact.count('.') < 2:
            return generate_fact()

        fact = fact[:fact.find("\n")]
        fact = fact[:fact.rfind(".") + 1]
        while fact.count(".") > 2 or len(fact) > 280:
            fact = fact[:fact.rfind(".", 0, fact.rfind(".")) + 1]
        fact = clean(fact)
        unwanted_chars = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')

        return fact if fact.find(".") != -1 and not is_content_offensive_or_invalid(fact) and unwanted_chars.search(
            fact) == None and not any(x in fact.lower() for x in [
                " dog ", " dogs ", " rat ", " rats ", " mouse ", " bitch ", " bitches ", " mice ",
                " shark ", " sharks "
            ]) and any(x in fact.lower() for x in [
                "cat ", "cats ", "cat.", "cats.", "cats'", "cat's", "kitten", "kitties", "kitty",
                "feline", "lion", "tiger", "cheetah"
            ]) else generate_fact()

    new_fact = f"{generate_fact()} #ai #catfacts"

    logging.info(new_fact)
    logging.info('Posting content.')
    tweet(new_fact)


def tweet(fact):
    api = get_api()

    number = true_random_randint(0, 3)
    if number == 1:
        media_object = upload_cat_image()
        api.update_status(status=fact, media_ids=[media_object.media_id])
    else:
        api.update_status(status=fact)