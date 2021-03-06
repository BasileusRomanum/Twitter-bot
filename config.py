import tweepy
import os
import logging

logger = logging.getLogger()

def create_api():
    #Access data are set here instead of as an environmental variables due to it being simpler for mobilitys sake
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error during API creation", exc_info=True)
        raise e

    logger.info("API created")
    return api
