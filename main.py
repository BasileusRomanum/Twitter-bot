import logging
import config
import functionalities as funk

def main():
    api = config.create_api()
    #funk.dmy(api, True)
    funk.dmyKursorem(api)
main()
