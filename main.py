from configparser import ConfigParser
import google
from flask import Flask
from flask_restful import Resource, Api, reqparse
from google.oauth2 import id_token
from google.auth.transport import requests
import time
import RequestBuilder
from RequestBuilder import Error, RequestBuilder
import database.database
from database.database import db, Player, TopScores
from google.cloud import exceptions

credentialsFile = "./credentials.ini"
credentials_web = ConfigParser()
credentials_web.read(credentialsFile)
CLIENT_ID = credentials_web.get('main', 'WEBAPI_CLIENT')

app = Flask(__name__)
api = Api(app)


add_parser = reqparse.RequestParser()
add_parser.add_argument('score', type=int)
add_parser.add_argument('key', type=str)
class AddScore(Resource):
    def post(self):
        args = add_parser.parse_args()
        score = args['score']
        key = args['key']

        UID = Validate(key)
        if UID is not None:
            doc_ref = db.collection(u'players').document(UID)
            try:
                doc = doc_ref.get().to_dict()
                player = Player(doc['username'], doc['scores'])
                player.scores.append((time.time(), score))

                doc_ref.set({u'username':player.username,u'scores':player.scores})
                return RequestBuilder.buildrequest({"success":True}, None)
            except exceptions.NotFound:
                error = Error.DOCUMENT
        else:
            error = Error.UID
        return RequestBuilder.buildrequest('',UID)


top_score_parser = reqparse.RequestParser()
top_score_parser.add_argument('start', type=int, default=0)
top_score_parser.add_argument('end', type=int)
class GetTopScores(Resource):
    def get(self):
        args = top_score_parser.parse_args()
        doc_ref = db.collection(u'topscores').stream()
        try:
            data = []
            for doc in doc_ref:
                info = doc.to_dict()
                tmp = [info['score'], info['uid'], info['date']]
                data.append(tmp)
            scores = TopScores(data)
            if args['end']:
                return RequestBuilder.buildrequest(scores.get_scores_sorted()[args['start']:args['end']], None)
            return RequestBuilder.buildrequest(scores.get_scores_sorted()[args['start']], None)
        except exceptions.NotFound:
            error = Error.DOCUMENT
        return RequestBuilder.buildrequest('',error)


player_parser = reqparse.RequestParser()
player_parser.add_argument('id')
class GetPlayer(Resource):
    def get(self):
        args = player_parser.parse_args()
        if args['id']:
            doc_ref = db.collection(u'players').document(args['id'])
            try:
                data = doc_ref.get().to_dict()
                player = Player(data['username'], data['scores'])
                return RequestBuilder.buildrequest(player, None)
            except exceptions.NotFound:
                error = Error.DOCUMENT
        else:
            error = Error.UID
        return RequestBuilder.buildrequest('', error)


player_scores_parser = reqparse.RequestParser()
player_scores_parser.add_argument('id')
player_scores_parser.add_argument('start', type=int, default=0)
player_scores_parser.add_argument('end', type=int)
class GetPlayerScores(Resource):
    def get(self):
        args = player_scores_parser.parse_args()
        if args['id']:
            doc_ref = db.collection(u'players').document(args['id'])
            try:
                data = doc_ref.get().to_dict()
                player = Player(data['username'], data['scores'])
                if args['topend']:
                    scores = player.get_top_scores(args['cutoff'], args['topend'])
                else:
                    scores = player.get_top_scores(args['cutoff'])
                return RequestBuilder.buildrequest(scores, None)
            except exceptions.NotFound:
                error = Error.DOCUMENT
        else:
            error = Error.UID
        return RequestBuilder.buildrequest('', error)


class Test(Resource):
    def get(self):
        return {"TEST":"SUCCESSFUL"}


def Validate(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid Token Issuer...')
        return idinfo['sub']
    except ValueError:
        return None


api.add_resource(Test, "/test")
api.add_resource(AddScore, "/addscore")  ## https://touchcrawler.appspot.com/addscore?key=XXXXXXXXXXXXXXXXXX&score=
api.add_resource(GetPlayer, "/player") ## https://touchcrawler.appspot.com/player?id=XXXXXXXXXXXXXXXXXX
api.add_resource(GetPlayerScores, "/playerscores") ## https://touchcrawler.appspot.com/player?id=XXXXXXXXXXXXXXXXXX&start=XXXXXXXXXXXXXXXXXX&end=XXXXXXXXXXXXXXXXXXXXX
api.add_resource(GetTopScores, "/topscores") ## https://touchcrawler.appspot.com/topscores?start=XXXXXXXXXXXXXXXXXX&end=XXXXXXXXXXXXXXXXXXXXX  ## end is optional