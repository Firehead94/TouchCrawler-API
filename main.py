from configparser import ConfigParser
import firebase_admin
import google
from flask import Flask
from flask_restful import Resource, Api, reqparse
from google.oauth2 import id_token
from google.auth.transport import requests
from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate('./touchcrawler-firebase-adminsdk-jbfj7-3950b63662.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

credentialsFile = "./credentials.ini"
credentials_web = ConfigParser()
credentials_web.read(credentialsFile)
CLIENT_ID = credentials_web.get('main', 'WEBAPI_CLIENT')

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('score', type=int)
parser.add_argument('key', type=str)


class AddScore(Resource):
    def post(self):
        args = parser.parse_args()
        score = args['score']
        key = args['key']

        UID = Validate(key)
        if UID is not None:
            doc_ref = db.collection(u'userScores').document(UID)
            try:
                doc = doc_ref.get()
                scores = doc.to_dict()
                scores[time.time()] = score
                doc_ref.set(scores)
                return scores
            except google.cloud.expections.NotFound:
                return "no document found"
        else:
            return {"error":"NoDoc Found"}


class GetScores(Resource):
    def get(self):
        doc_ref = db.collection(u'userScores').stream()
        scores = {}
        for doc in doc_ref:
            UID = doc.id
            info = doc.to_dict()
            scores[UID] = info
        return scores


class Test(Resource):
    def get(self):
        return {"TEST":"SUCCESSFUL"}


class GetTopScores(Resource):
    def get(self):
        doc_ref = db.collection(u'scores').document("top")
        try:
            doc = doc_ref.get()
            return doc.to_dict()
        except:
            return {"error":"NoDoc Found"}


def Validate(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid Token Issuer...')
        return idinfo['sub']
    except ValueError:
        return None


api.add_resource(AddScore, "/newscore")  ## https://touchcrawler.appspot.com/newscore?key=XXXXXXXXXXXXXXXXXX&score=
api.add_resource(GetScores, "/scores")
api.add_resource(GetScores, "/scores/top")
api.add_resource(Test, "/test")