from flask import Flask, request
from flask_restful import Resource, Api
from configparser import ConfigParser
import sqlalchemy

app = Flask(__name__)
api = Api(app)
credentialsFile = "credentials.ini"
credentials = ConfigParser()
credentials.read(credentialsFile)

DB_USER = credentials.get('main', 'DB_USER')
DB_PASS = credentials.get('main', 'DB_PASS')
DB_NAME = credentials.get('main', 'DB_NAME')
DB_CLOUD_CONN_NAME = credentials.get('main', 'DB_CONN_NAME')


# [START cloud_sql_mysql_sqlalchemy_create]
# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        query={"unix_socket": "/cloudsql/{}".format(DB_CLOUD_CONN_NAME)},
    ),
    # ... Specify additional properties here.
    # [START_EXCLUDE]
    # [START cloud_sql_mysql_sqlalchemy_limit]
    # Pool size is the maximum number of permanent connections to keep.
    pool_size=5,
    # Temporarily exceeds the set pool_size if no connections are available.
    max_overflow=2,
    # The total number of concurrent connections for your application will be
    # a total of pool_size and max_overflow.
    # [END cloud_sql_mysql_sqlalchemy_limit]
    # [START cloud_sql_mysql_sqlalchemy_backoff]
    # SQLAlchemy automatically uses delays between failed connection attempts,
    # but provides no arguments for configuration.
    # [END cloud_sql_mysql_sqlalchemy_backoff]
    # [START cloud_sql_mysql_sqlalchemy_timeout]
    # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
    # new connection from the pool. After the specified amount of time, an
    # exception will be thrown.
    pool_timeout=30,  # 30 seconds
    # [END cloud_sql_mysql_sqlalchemy_timeout]
    # [START cloud_sql_mysql_sqlalchemy_lifetime]
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    # Connections that live longer than the specified amount of time will be
    # reestablished
    pool_recycle=1800,  # 30 minutes
    # [END cloud_sql_mysql_sqlalchemy_lifetime]
    # [END_EXCLUDE]
)
# [END cloud_sql_mysql_sqlalchemy_create]

class Test(Resource):
    def get(self):
        return {'status':'success'}

class DBTest(Resource):
    def get(self):
        names = []
        with db.connect() as conn:
            result = conn.execute("SELECT firstName FROM accounts").fetchall()
        for row in result:
            names.append({"FirstName" : row[0]})

        return names


api.add_resource(Test, '/')
api.add_resource(DBTest, "/DB")