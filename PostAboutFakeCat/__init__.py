import logging
import re
import io
import tempfile
import os.path
import random

from urllib.request import Request, urlopen
from ..utils import clean, get_api, is_content_offensive, get_generated_response, true_random_randint, true_random_choice

import azure.functions as func

prompts = [
    "This is the coolest cat. My algorithms tell me it", "This cat is named", "This is a cat that",
    "You might not believe it, but my algorithms tell me this cat",
    "My advanced AI tells me that this cat", "I've computed that when this cat named", "Cats are amazing. This cat named", 
    "My algorithms tell me that this cat", "I've computed that this cat", "My advanced AI has determined that this cat", 
    "My algorithms tell me that this cat named", "I've computed that this cat named", "My advanced AI has determined that this cat named", "The story behind this cat is",
    "This famous cat once", "In 1975, this cat", "This cat, in 1843,", "The first was his son Tad’s cat, Tabby. Apparently, Lincoln enjoyed feeding Tabby with a gold fork at White House dinners.",
    "For several generations, a group of six-toed cats has taken up residence at Ernest Hemingway’s former Key West home. They are apparently descendants of Snowball, a fluffy white cat who was a gift to the Hemingways.",
    "Scarlett was a stray cat living in Brooklyn, New York who rose to fame after risking her life to save her kittens from a fire in 1996.",
    "Choupette Lagerfeld is totally living the dream. Not only is her human, Karl Lagerfeld, famous and rich, but she and Karl adore each other.",
    "Talk about a science experiment. The cat named Little Nicky is the first commercially produced cat clone, produced from the DNA of a 19-year-old Maine Coon who died in 2003.",
    "This cat named Unsinkable Sam went down in history for surviving three major shipwrecks. The first was the German Battleship Bismarck, sunk by the British in 1941.",
    "Snowball belonged to a Canadian couple who lived on Prince Edward Island with their son, Douglas Beamish.",
    "Once known as the internet’s most famous cat, Japanese feline Maru earned his fame in 2007 from YouTube.",
    "If you’ve seen the Austin Powers movie series, you’ve seen Dr. Evil’s hairless cat, Mr. Bigglesworth.",
    "Oscar is the tortoiseshell cat who has made national headlines for the last decade due to his uncanny ability to predict death.",
    "Tommaso, once a poor stray cat roaming the streets, was rescued by a very wealthy woman named Maria Assunta who loved him dearly.",
    "Tardar Sauce quickly rose to internet fame because of her face, which looks permanently grumpy. Her owner’s brother posted a photo of her cat on Reddit in 2012, and the rest is history."
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
            generated_prompt = get_generated_response(promts_promt, 200)
            generated_prompt = generated_prompt.split('\n\n')[1]
            generated_prompt = clean(generated_prompt)

            if is_content_offensive(generated_prompt):
                logging.info("Offensive prompt content." + generated_prompt)
                return get_prompt()
        
            if len(generated_prompt) < 10:
                logging.info("Prompt too short. " + generated_prompt)
                return get_prompt()
            
            if not any(x in generated_prompt.lower() for x in [
                "cat ", "cat ", "cats ", "cat.", "cats.", "cats'", "cat's", "kitten", "kitties", "kitty",
                "feline", "lion", "tiger", "cheetah"
            ]):
                logging.info("Prompt doesn't mention cat. " + generated_prompt)
                return get_prompt()

            return generated_prompt
        except:
            return get_prompt()
        
    return get_prompt()

def main(mytimer: func.TimerRequest) -> None:

    number = true_random_randint(0, 75)
    if number != 1:
        logging.info(str(number) + " Doesn't feel right to post.")
        return

    api = get_api()

    prompt = get_generated_prompt(api)

    generate_count = 0

    def get_catinfo():

        nonlocal generate_count
        generate_count = generate_count + 1
        if generate_count > 20:
            raise Exception('generation limit hit')

        reply = get_generated_response(prompt, 240)
        reply = reply[:reply.rfind("\n")]
        reply = reply[:reply.rfind(".") + 1]
        reply = clean(f"{prompt} {reply}")

        if len(reply) < 20:
            return get_catinfo()

        regex = re.compile('[\[\]@_#$%^&*()<>/\|}{~:]')
        if regex.search(reply) is not None or is_content_offensive(reply):
            return get_catinfo()

        return f"{reply} #ai #catsoftwitter"

    info = get_catinfo()
    logging.info(info)

    logging.info("Downloading image.")

    request = Request('https://thiscatdoesnotexist.com/', headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urlopen(request) as url:
            data = url.read()
            image = io.BytesIO(data)
            with tempfile.TemporaryDirectory() as td:
                file_name = os.path.join(td, "cat.jpg")
                with open(file_name, 'wb') as out:
                    out.write(image.read())
                media_object = api.media_upload(file_name)
                api.update_status(status=info, media_ids=[media_object.media_id])
                logging.info("Posted.")
    except Exception as e:
        logging.info(e)
