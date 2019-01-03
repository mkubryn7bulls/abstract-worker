from random import randint
from time import sleep

from handler.persist import SimplePersistingHandler


class LighthouseCalculateScoreHandler(SimplePersistingHandler):

    def prepare_data_to_persist(self, payload):
        return self.calculate_score(payload)

    @staticmethod
    def calculate_score(url: str):
        print('Calculating lighthouse score for url', url)
        sleep(3)
        return "%s -> %s" % (url, randint(0, 100))
