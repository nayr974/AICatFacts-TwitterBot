import logging
import re
import os
import io
import random

from urllib.request import Request, urlopen
from ..utils import clean, get_api, is_content_offensive, get_generated_response

import azure.functions as func

prompts = [
    "This cat", "This cat is named", "This is a cat named", "This is a cat that",
    "You might not believe it, but this cat", "A cat named"
]

def main(mytimer: func.TimerRequest) -> None:
    api = get_api()

    prompt = random.choice(prompts)

    generate_count = 0

    def get_catinfo():

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 20:
            raise Exception('generation limit hit')

        reply = get_generated_response(prompt, 160)
        reply = reply[:reply.find("\n")]
        reply = reply[:reply.rfind(".") + 1]
        reply = clean(reply)

        if len(reply) < 20:
            return get_catinfo()

        regex = re.compile('[@_#$%^&*()<>/\|}{~:]')
        if regex.search(reply) is not None and not is_content_offensive(reply):
            return get_catinfo()

        return f"{prompt} {reply} #ai #catsoftwitter #caturday"

    info = get_catinfo()

    logging.info("Downloading image.")

    request = Request('https://thiscatdoesnotexist.com/', headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urlopen(request) as url:
            image = io.BytesIO(url.read())
            api.update_with_media('cat.jpg', status=info, file=image)
            logging.info("Posted.")
    except Exception as e:
        logging.info(e)
