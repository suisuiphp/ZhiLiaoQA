#encoding:utf-8
import os

DEBUG = False

SECRET_KEY = os.urandom(24)

#dialect+driver://username:password@host:port/database

DIALECT="mysql"
DRIVER="mysqldb"
USERNAME="root"
PASSWORD="123456"
# HOST="127.0.0.1"
HOST="localhost"
PORT="3306"
DATABASE="db_flask"
URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI=URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
