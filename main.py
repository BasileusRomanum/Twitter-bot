import tweepy
import logging
import config
from time import sleep
#import functionalities as funk
import random
from quotes import cytaty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    #Api creation
    api = config.create_api()
    result = []
    while True:
        try:
            for i in range(0, len(cytaty)):
                result.append(cytaty[i][random.randint(0, len(cytaty[i])-1)])
        except:
            logger.info("Korwin quote could not be generated")
            result.clear()
            continue
        logger.info("Korwin quote generated")
        if len("Korwin quote for now: " + '"' + " ".join(result) + '"') <=280:
            api.update_status("Korwin quote for now: " + '"' + " ".join(result) + '"')
            logger.info("Korwin quote has been sent to twitter")
            result.clear()
            sleep(60)
        else:
            logging.info("Character limit exceeded.")
            result.clear()
            continue

main()
