import tweepy
import logging
import random
import json
from time import sleep
from quotes import cytaty

logger = logging.getLogger()


def followFollowers(api):
    logger.info("Odczytywanie i followowanie followersów")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Śledzenie {follower.name}")
            follower.follow()

class Favoryzuj(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Przetwarzanie tweeta o id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            return

        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Błąd podczas lubienia", exc_info=True)

        if not tweet.retweeted:
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Błąd podczas podawania dalej", exc_info=True)

    def on_error(self, status):
        logger.error(status)

#Generator of "quotes" by infamous polish politician.
def korwinizmy():
    hasztagi = '\n#Korwin #MyslDnia'
    while True:
        try:
            for i in range(0, len(cytaty)):
                result.append(cytaty[i][random.randint(0, len(cytaty[i])-1)])
        except:
            logger.info("Error during creating Korwin's quote")
            result.clear()
            continue
        logger.info("Korwin quote generated")
        if len("Myśl według Korwina na teraz: " + '"' + " ".join(result) + hasztagi) <=280:
            api.update_status("Myśl według Korwina na teraz: " + '"' + " ".join(result) + hasztagi)
            logger.info("Korwinizm został umieszczony na twitterze")
            result.clear()
            sleep(60)
        else:
            logger.error("Character limit exceeded")
            result.clear()
            continue

#Monitoring of dms through while loop
def dmy(api, flaga=False):
    odpowiedziane = []
    answerText = "Example string"
    while True:
        dmy = api.list_direct_messages()
        print(type(dmy))
        for message in dmy:
            if message.created_timestamp not in odpowiedziane:
                try:
                    odpowiedziane.append(message.created_timestamp)
                    print(message.message_create['sender_id'])
                    api.send_direct_message(message.message_create['sender_id'], answerText)
                except:
                    logger.error("Error during answering to a message", exc_info=True)
                    sleep(random.randint(1,5))
                    pass
        if flaga:
            break
        sleep(5)

#As to not use while loop monitoring dms has been rewritten to use Cursor object.
#And it works. Although, I seem to be unable to access dm's text this way. Why should I tho, I don't know.
#I've just been trying to do it 'till I've askedy myself "Why?"
def dmyKursorem(api):
#Local variables
    has_been_answered = False
    dm_answer = "Hello beatiful person!"
    logger.info("Trying to load messages id")
#Loading up json with already answered messages. And if it's empty, then create an empty dictionary
    try:
        messagesDictionary = json.load(open('msgID.json'))
        logger.info("IDs loaded sucesfully")
    except ValueError:
        messagesDictionary = {}

        logger.error("Unable to load from msgID.json. Created empty dictionary", exc_info=True)
    #Json that temp. stores id and timestamp of each dm that has been responded too.
    #It's gonna be later dumped into a file.
    for dm in tweepy.Cursor(api.list_direct_messages).items():
        for storedMessage in messagesDictionary.items():
            if dm.id == storedMessage['id']:
                has_been_answered = True
                break
        if not has_been_answered:
            api.send_direct_message(dm.message_create['sender_id'], dm_answer)
            messagesDictionary["".join(['message', time.time()])] = {'id':dm.id, 'timestamp':dm.timestamp}
            open("msgID.json", 'w').write(messagesDictionary)
