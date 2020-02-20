from configparser import ConfigParser
import firebase_admin
from Tools.scripts import google
from flask import Flask
from flask_restful import Resource, Api, reqparse
from database.connection import db
from google.oauth2 import id_token
from google.auth.transport import requests
from firebase_admin import credentials, firestore
import time

cred = credentials.Certificate('./touchcrawler-firebase-adminsdk-jbfj7-3950b63662.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

credentialsFile = "credentials.ini"
credentials_web = ConfigParser()
credentials_web.read(credentialsFile)

CLIENT_ID = credentials_web.get('main', 'WEBAPI_CLIENT')
web_app = Flask(__name__)
api = Api(web_app)
parser = reqparse.RequestParser()
parser.add_argument('score', type=int)
parser.add_argument('key', type=str)



class AddScore(Resource):
    def post(self):
        args = parser.parse_args()
        score = args['score']
        key = args['key']

        UID = Validate(key)
        print(UID)
        if UID is not None:
            doc_ref = db.collection(u'userScores').document(UID)
            try:
                doc = doc_ref.get()
                scores = doc.to_dict()
                scores[time.time()] = score
                doc_ref.set(scores)
                print(scores)
            except google.cloud.expections.NotFound:
                print("no document found")



def Validate(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid Token Issuer...')

        return idinfo['sub']

    except ValueError:
        return None



api.add_resource(AddScore, "/newscore")  ## /newscore?key=XXXXXXXXXXXXXXXXXX&score=