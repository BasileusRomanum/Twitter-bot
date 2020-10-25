import tweepy
import logging
import time

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


cytaty = [
    ['Proszę zwrócić uwagę, że',
    'I tak mam trzy razy mniej czasu, więc proszę mi pozwolić powiedzieć, że',
    'Państwo się śmieją, ale', 'Ja nie potrzebowałem edukacji seksualnej, żeby wiedzieć, że',
    'No niestety',
    'Gdzie leży przyczyna problemu? Ja państwu powiem:',
    'Państwo chyba nie widzą, że',
    'Oświadczam kategorycznie:',
    'Powtarzam',
    'Powiedzmy z całą mocą:',
    'W Polsce dzisiaj',
    'Państwo sobie nie zdają sprawy, że',
    'To ja przepraszam bardzo:',
    'Otóż nie wiem, czy pan wie, że',
    'Yyyyyy...',
    'Ja chcę powiedzieć jedną rzecz:',
    'Trzeba powiedzieć jasno',
    'Jak powiedział wybitny krakowianin,',
    'Proszę mnie dobrze zrozumieć',
    'Ja chciałem państwu przypomnieć, że',
    'Niech państwo nie mają złudzeń:',
    'Powiedzmy to wyraźnie:'],
    ['właściciele niewolników',
    'związkowcy',
    'trockiści', 'tak zwane dzieci kwiaty', 'rozmaici urzędnicy', 'federaści', 'etatyści', 'ci durnie i złodzieje', 'ludzie wybrani głosami meneli spod budki z piwem', 'socjaliści pobożni', 'socjaliści bezbożni', 'komuniści z krzyżem w zębach', 'agenci obcych służb', 'członkowie Bandy Czworga', 'pseudo-masoni z Wielkiego Wschodu Francji', 'przedstawiciele czerwonej hołoty', 'ci wszyscy (tfu) geje', 'funkcjonariusze reżymowej telewizj', 'tak zwani ekolodzy', 'ci wszyscy (tfu) demokracji', 'agenci bezpieki', 'feminazistki'],
    ['po przeczytaniu Manifestu Komunistycznego', 'którymi się brzydzę', 'których nienawidzę', 'z okolic Gazety Wyborczej', 'czyli taka żydokomuna', 'odkąd zniesiono karę śmierci', 'którymi pogardzam', 'któych miejsce w normalnym kraju jest w więzieniu', 'na polecenie Brukseli', 'posłusznie', ' bezmyślnie', 'z nieprawdopodobną pogardą dla człowieka', 'za pieniądze podatników', 'zgodnie z ideologią LGBTQZ', 'za wszelką cenę', 'zupełnie bezkarnie', 'całkowicie bezczelnie', 'o poglądach na lewo od komunizmu', 'celowo i świadomie', 'z premedytacją', 'od czasów Okrągłego Stołu', 'w ramach postępu'],
    ['udają homoseksualistów', 'niszczą rodzinę', 'idą do polityki', 'zakazują góralom robienia oscypków', 'organizują paraolimpiady', 'wprowadzają ustrój w którym raz na cztery lata można wybrać sobie pana', 'ustawiają fotoradary', 'wprowadzają dotacje', 'wydzielają buspasy', 'podnoszą wiek emerytalny', 'rżną głupa', 'odbierają dzieci rodzicom', 'wprowadzają absurdalne przepisy', 'umieszczają dzieci w szkołach koedukacyjnych', 'wprowadzają parytety', 'nawołują do podniesienia podatku', 'próbują wyrzucić kierowców z miast', 'próbują skłócić Polskę z Rosją', 'głoszą brednie o globalnym ociepleniu', 'zakazują posiadania broni', 'nie dopuszczają prawicy do władzy', 'uczą dzieci homoseksualizmu'],
    ['żeby poddawać wszystkich tresurze', 'bo taka jest ich natura', 'bo chcą wszystko kontrolować', 'bo nie rozumieją, że socjalizm nie działa', 'żeby wreszcie zapanował socjalizm', 'dokładnie tak jak tow. Janosik', 'zamiast pozwolić ludziom zarabiać', 'żeby wyrwać kobiety z domu', 'bo tak jest w interesie tak zwanych ludzi pracy', 'zamiast pozwolić decydować konsumentowi', 'żeby nie opłacało się mieć dzieci', 'zamiast obniżyć podatki', 'bo nie rozumieją, że selekcja naturalna jest czymś dobrym', 'żeby mężczyźni przestali być agresywni', 'bo dzięki temu mogą brać łapówki', 'bo dzięki temu mogą kraść', 'bo dostają za to pieniądze', 'bo tak się uczy w państwowej szkole', 'bo bez tego (tfu) demokracja nie może istnieć', 'bo głupich jest więcej niż mądrych', 'bo chcą tworzyć raj na Ziemi', 'bo chcą niszczyć cywilizację białego człowieka'],
    ['co ma zresztą tyle samo sensu, co zawody w szachach dla debili.', 'co zostało dokładnie zaplanowane w Magdalence przez śp. generała Kiszczaka.', 'i trzeba być idiotą, żeby ten system popierać.', 'ale nawet ja jeszcze dożyję normalnych czasów.', 'co dowodzi, że wyskrobano nie tych, co trzeba.', 'a zwykłym ludziom wmawiają, że im coś "dadzą".', '- cóż: chcieliście (tfu) demokracji, to macie.', 'dlatego trzeba zlikwidować koryto, a nie zmieniać świnie.', 'a wystarczyłoby przestać wypłacać zasiłki.', 'podczas gdy normalni ludzi uważani są za dziwaków.', 'co w wieku XIX po prostu by wyśmiano.', '- dlatego w społeczeństwie jest równość, a powinno być rozwarstwienie.', 'co prowadzi Polskę do katastrofy', '- dlatego trzeba przywrócić normalność.', 'ale w wolnej Polsce pójdą siedzieć.', 'przez kolejne kadencje.', 'o czym się nie mówi.', 'i właśnie dlatego Europa umiera.', 'ale przyjdą muzułmanie i zrobią porządek.', '- tak samo zresztą jak za Hitlera.', '- proszę zobaczyć, co się dzieje na Zachodzie, jeśli mi państwo nie wierzą.', 'co lat temu sto nikomu nie przyszłoby nawet do głowy']]
