import logging
import time
import io
import os
import os.path
import tempfile
import re
import requests
import json
import tweepy
import quantumrand
import random
from profanity_check import predict
from better_profanity import profanity
from datetime import datetime, timedelta
from urllib.request import Request, urlopen


def true_random_randint(min, max):

    #Azure linux VM defaults to cipher that API rejects
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    
    try:
        return quantumrand.randint(min, max)
    except:
        return random.SystemRandom().randint(min, max)


def true_random_choice(list):
    return list[true_random_randint(0, len(list) - 1)]


def empty_string(match):
    return ''


def single_space(match):
    return ' '


def capitalize(text, delimiter):
    split_text = [sentence[0].upper()+sentence[1:] for sentence in text.split(delimiter)]
    return delimiter.join(split_text).replace(' ai ', ' A.I. ').replace(' a.i. ', ' A.I. ').replace(' ai. ', ' AI. ')


def clean(text):
    cleantext = text.replace('\n', ' ').replace(';', '.')
    cleantext = re.sub(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
        empty_string,
        cleantext,
        flags=re.IGNORECASE)
    cleantext = re.sub(r'@\w*|#\w*|<.*?>|\[.*?\]|[^\x00-\x7F]+',
                       empty_string,
                       cleantext,
                       flags=re.IGNORECASE)
    cleantext = re.sub(r'(\d+)\.', empty_string, cleantext, flags=re.IGNORECASE)
    cleantext = cleantext.replace('...', '. ').replace('..', '. ').replace('? ?', '? ').replace('(', ' ').replace(')', '. ').replace('"', '').replace(
        ',.', '. ').replace(' ,', ', ').replace(',  ', ', ').replace(' .', '.').replace(
            '.', '. ').replace('.  ', '. ').replace(' .', '.').replace(' !', '!').replace(
                '!', '! ').replace('!  ', '! ').replace(' ?', '?').replace('?', '? ').replace(
                    '?  ', '? ').replace(',,', ',').replace(
                        ' .', '.').replace(' s ', 's ').replace('. and', ', and').replace(
                            '?.', '?').replace('!.', '!').replace('? !', '?!').replace(
                                '! ?', '!?').replace(' ,', ',').replace(' s.', 's.').replace(
                                    ' s!', 's!').replace(' s?', 's?').replace(' s,', 's,').replace(
                                        ', e. g.', '.').replace('e. g.', '').replace(' \'', '\'').replace('.,', '.').replace('..', '.')
    cleantext = re.sub('\s{2,}', single_space, cleantext)
    cleantext = cleantext.strip()
    cleantext = capitalize(cleantext, '. ')
    cleantext = capitalize(cleantext, '! ')
    cleantext = capitalize(cleantext, '? ')
    cleantext = cleantext.replace('..', '.')
    return cleantext


def deploy_catfact_model():
    endpoint = os.environ['DEPLOY_URL']
    login_json = {
        "operationName":
        "LogInByPassword",
        "variables": {
            "email": os.environ['DEPLOY_CLIENT_ID'],
            "password": os.environ['DEPLOY_CLIENT_SECRET']
        },
        "query":
        "mutation LogInByPassword($email: String!, $password: String!) {\n  logIn(input: {email: $email, credentials: {password: $password}})\n}\n"
    }
    undeploy_at = datetime.utcnow() + timedelta(minutes=10)
    deploy_json = {
        "operationName":
        "DeployModel",
        "variables": {
            "input": {
                "id": os.environ['DEPLOY_MODEL_ID'],
                "autoUndeployAt": undeploy_at.isoformat() + 'Z'
            }
        },
        "query":
        "mutation DeployModel($input: DeployModelInput!) {\n  deployModel(input: $input) {\n    id\n    deploymentStage\n    autoUndeployAt\n    __typename\n  }\n}\n"
    }

    session = requests.Session()
    login_response = session.post(endpoint, json=login_json)

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "*/*",
        "content-type": "application/json",
        "x-csrf-token": session.cookies.get_dict()["trainer:csrf"]
    }

    time.sleep(1)
    session.post(endpoint, json=deploy_json, headers=headers)
    return


def get_generated_catfact(text):
    endpoint = os.environ['GENERATE_FACT_URL']
    json = {
        'prompt': {
            'text': text
        },
        'length': 180,
        'forceNoEnd': False,
        'topP': 0.8,
        'temperature': 1.25
    }
    token = os.environ['GENERATE_TOKEN']
    headers = {"Authorization": f"Bearer {token}"}
    responsejson = requests.post(endpoint, json=json, headers=headers).json()
    return responsejson["data"]["text"]


def get_generated_response(text, length, temp=0.9):
    endpoint = os.environ['GENERATE_REPLY_URL']
    json = {
        'prompt': {
            'text': text,
            'isContinuation': True
        },
        'length': length,
        'topP': 0.9,
        'temperature': temp
    }
    token = os.environ['GENERATE_TOKEN']
    headers = {"Authorization": f"Bearer {token}"}
    responsejson = requests.post(endpoint, json=json, headers=headers).json()
    return responsejson["data"]["text"]


def get_api():
    # personal details
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth_handler=auth,
                      retry_count=3,
                      timeout=20,
                      wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def upload_cat_image():
    cat_api_key = os.environ['CAT_API_KEY']
    cat_api_url = f'https://api.thecatapi.com/v1/images/search'
    responsejson = requests.get(
        cat_api_url,
        headers={
            'x-api-key':
            cat_api_key,
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
        }).json()
    cat_image_url = responsejson[0]["url"]

    with tempfile.TemporaryDirectory() as td:
        file_name = os.path.join(td, "cat.jpg")
        cat_image_request = Request(cat_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(cat_image_request) as url:
            data = url.read()
            image = io.BytesIO(data)
            with open(file_name, 'wb') as out:
                out.write(image.read())
                api = get_api()
                media_object = api.media_upload(file_name)
                return media_object


def is_content_offensive_or_invalid(content):
    if predict([content])[0] == 1:
        return True

    if re.search(offensive, content) is not None:
        return True

    if profanity.contains_profanity(content):
        return True

    #other unwanted words or phrases
    if any(x in content.lower() for x in [
            "blog", "click here", "raw data", "article", "dog", "puppy", "www", "link", "kill",
            "rape", "obama", "trump", "passed away", "died", "death", "passing of", "vet", "sick", 
            "in this paper", "download here", "a. ", "b. ", "1. ", "2. ", "read more", ".com", ". com ", 
            "check here", ". com.", " dr.", "bark", "cats a lot. you said", "podcast", "intercourse", "advertisement",
            "adopt", "shelter", ". pic.", ". twitter.", "reddit", "all rights reserved", "this post"
    ]):
        return True

    return False


offensive = re.compile(
    r"\b(deaths?|dead(ly)?|die(s|d)?|hurts?|(sex(ual(ly)?)?|"
    r"child)[ -]?(abused?|trafficking|"
    r"assault(ed|s)?)|injur(e|i?es|ed|y)|kill(ing|ed|er|s)?s?|"
    r"wound(ing|ed|s)?|fatal(ly|ity)?|"
    r"shoo?t(s|ing|er)?s?|crash(es|ed|ing)?|attack(s|ers?|ing|ed)?|"
    r"murder(s|er|ed|ing)?s?|"
    r"fuck(s|ing)?|shit|cunt|bitch|ass|dick|"
    r"hostages?|(gang)?rap(e|es|ed|ist|ists|ing)|assault(s|ed)?|"
    r"pile-?ups?|massacre(s|d)?|"
    r"assassinate(d|s)?|sla(y|in|yed|ys|ying|yings)|victims?|"
    r"tortur(e|ed|ing|es)|"
    r"execut(e|ion|ed|ioner)s?|gun(man|men|ned)|suicid(e|al|es)|"
    r"bomb(s|ed|ing|ings|er|ers)?|"
    r"mass[- ]?graves?|bloodshed|state[- ]?of[- ]?emergency|al[- ]?Qaeda|"
    r"blasts?|violen(t|ce)|"
    r"lethal|cancer(ous)?|stab(bed|bing|ber)?s?|casualt(y|ies)|"
    r"sla(y|ying|yer|in)|"
    r"drown(s|ing|ed|ings)?|bod(y|ies)|kidnap(s|ped|per|pers|ping|pings)?|"
    r"rampage|beat(ings?|en)|"
    r"terminal(ly)?|abduct(s|ed|ion)?s?|missing|behead(s|ed|ings?)?|"
    r"homicid(e|es|al)|"
    r"burn(s|ed|ing)? alive|decapitated?s?|jihadi?s?t?|hang(ed|ing|s)?|"
    r"funerals?|traged(y|ies)|"
    r"autops(y|ies)|child sex|sob(s|bing|bed)?|pa?edophil(e|es|ia)|"
    r"9(/|-)11|Sept(ember|\.)? 11|"
    r"genocide)\W?\b",
    flags=re.IGNORECASE)
