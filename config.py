import tweepy
import os
import logging

logger = logging.getLogger()

def create_api():
    #Jebaj się sam z ustawianiem tego jako zmienne środowiskowe w windowsie. Aj der ju.
    consumer_key = "ZMOlk9qCm2sSCpZcWVRAIVkbT"
    consumer_secret = "DscKgmlRE7RjtLMfqRR83yXvPbgRaELn306rXBSZ7zA93AbThr"
    access_token = "1318235514273746945-BzsD4vvlsxMGdAvKquyWmPSuJ5g9BR"
    access_token_secret = "jkd57SxHAfp5sqa57KCK91Tbbun7YtQTzkhOEfJfbeHcv"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Błąd podczas tworzenia API", exc_info=True)
        raise e

    logger.info("API stworzone")
    return api
