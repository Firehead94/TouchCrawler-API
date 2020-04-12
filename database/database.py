import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import typing
import operator


cred = credentials.Certificate('./touchcrawler-firebase-adminsdk-jbfj7-3950b63662.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


class Player:

    def __init__(self, username, scores = []):
        self.username = username
        self.scores = scores

    def get_scores_sorted(self):
        return sorted(self.scores, key=operator.itemgetter(1))

    def get_top_scores(self, cutoff = 0, topend: typing.Optional = 0):
        if cutoff == 0:
            return self.get_scores_sorted()
        return self.get_scores_sorted()[topend:cutoff]


class TopScores:

    def __init__(self, scores = []):
        self.scores = scores

    def get_scores_sorted(self):
        return sorted(self.scores, key=operator.itemgetter(1))

