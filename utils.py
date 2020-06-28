import logging
import time
import os
import re
import requests
import json
import tweepy
from profanity_check import predict
from datetime import datetime, timedelta


def clean(text):
    cleanr = re.compile('@\w*|#\w*|<.*?>|\[.*?\]|[^\x00-\x7F]+')
    cleantext = re.sub(cleanr, '', text).strip().replace('\n', ' ').replace('"', '')
    cleantext = re.sub('\s{2,}', ' ', cleantext)
    return cleantext.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(
        '!', '! ').replace('!  ', '! ').replace(' ?', '?').replace('?', '? ').replace('?  ', '? ')
        
def deploy_catfact_model():
    endpoint = os.environ['DEPLOY_URL']"
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
    undeploy_at = datetime.utcnow() + timedelta(minutes=30)
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
        'length': 200,
        'forceNoEnd': False,
        'topP': 0.4,
        'temperature': 1.76
    }
    token = os.environ['GENERATE_TOKEN']
    headers = {"Authorization": f"Bearer {token}"}
    responsejson = requests.post(endpoint, json=json, headers=headers).json()
    return responsejson["data"]["text"]


def get_generated_response(text, length):
    endpoint = os.environ['GENERATE_FACT_URL']
    json = {'prompt': {'text': text, 'isContinuation': True}, 'length': length}
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
    return tweepy.API(
        auth_handler=auth,
        retry_count=3,
        timeout=20,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)


def is_content_offensive(content):
    logging.info(predict([content])[0])
    if predict([content])[0] == 1:
        return True

    if re.search(offensive, content) is not None:
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
    r".*trump|.*obama|"
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
