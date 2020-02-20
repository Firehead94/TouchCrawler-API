from configparser import ConfigParser
import firebase_admin
from flask import Flask
from flask_restful import Resource, Api
from database.connection import db
from google.oauth2 import id_token
from google.auth.transport import requests
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./touchcrawler-firebase-adminsdk-jbfj7-3950b63662.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

credentialsFile = "credentials.ini"
credentials_web = ConfigParser()
credentials_web.read(credentialsFile)

CLIENT_ID = credentials_web.get('main', 'WEBAPI_CLIENT')
web_app = Flask(__name__)
api = Api(web_app)


class Test(Resource):
    def get(self):
        return {'status':'success'}

class DBTest(Resource):
    def get(self):
        names = []
        DBconnection = False
        with db.connect() as conn:
            result = conn.execute("SELECT firstName FROM accounts").fetchall()
        for row in result:
            DBconnection = True

        return {"DB_Connection":DBconnection}

class Validate(Resource):
    def post(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid Token Issuer...')

            userid = idinfo['sub']
            print(f"userid = {userid}")
        except ValueError:
            pass



api.add_resource(Validate, "/validate?=")
api.add_resource(Test, '/')
api.add_resource(DBTest, "/DB")