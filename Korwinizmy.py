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
    #Tworzymy api
    api = config.create_api()
    result = []
    #Lista, która ma przechowywać id tweetów, do których już odpowiedzieliśmy
    #Tę pętlę chyba dałoby radę zastąpić streamem, ale nie chce mi się teraz tego rozkminiać. uwu
    while True:
        try:
            for i in range(0, len(cytaty)):
                result.append(cytaty[i][random.randint(0, len(cytaty[i])-1)])
        except:
            logger.info("Błąd podczas generowania korwinizmu")
            result.clear()
            continue
        logger.info("Wygenerowano korwinizm")
        if len("Myśl według Korwina na teraz: " + '"' + " ".join(result) + '"') <=280:
            api.update_status("Myśl według Korwina na teraz: " + '"' + " ".join(result) + '"')
            logger.info("Korwinizm został umieszczony na twitterze")
            result.clear()
            sleep(60)
        else:
            logging.info("Przekroczono limit znaków.")
            result.clear()
            continue

main()
