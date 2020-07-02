import logging
import re
import random

from datetime import datetime
from ..utils import clean, get_api, get_generated_catfact
from .catfacts import facts

import azure.functions as func


def get_seed_facts():
    split_facts = facts.split("\n")
    seed_facts = [
        random.choice(split_facts),
        random.choice(split_facts),
        random.choice(split_facts),
        random.choice(split_facts),
        random.choice(split_facts),
        random.choice(split_facts),
        random.choice(split_facts)
    ]
    return "FACT: " + "\nFACT: ".join(seed_facts) + "\n"


def main(mytimer: func.TimerRequest) -> None:
    prompt = get_seed_facts()

    generate_count = 0

    def generate_fact():

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 20:
            raise Exception('generation limit hit')

        logging.info('Generating fact.')
        fact = get_generated_catfact(prompt)
        fact = fact[:fact.find("\n")]
        fact = fact[:fact.rfind(".") + 1]
        fact = clean(fact)
        logging.info(fact)

        unwanted_chars = re.compile('[@_#$%^&*<>/\|}{~:-]')

        return fact if fact.find(".") is not None and unwanted_chars.search(fact) == None and any(
            x in fact.lower() for x in [
                "cat ", "cats ", "cat.", "cats.", "cats'", "kitten", "feline", "lion", "tiger",
                "cheetah"
            ]) else generate_fact()

    new_fact = generate_fact() + ' #ai #cats'

    logging.info('Posting content.')
    tweet(new_fact)


def tweet(fact):
    api = get_api()
    api.update_status(status=fact)
