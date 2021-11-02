import urllib
import os

class Config:
    SECRET_KEY  = os.environ.get('SECRET_KEY')
    DB_NAME = os.environ.get('DB_SERVER_NAME')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    DB_USER_ID = os.environ.get('DB_USER_ID')
    DB_USER_PASSWORD = os.environ.get('DB_USER_PASS')

    # SQLALCHEMY_DATABASE_URI  = 'sqlite:///cooklab.db'
    connection = 'DRIVER={SQL Server};' + f'SERVER={DB_NAME};DATABASE={DB_DATABASE};UID={DB_USER_ID};PWD={DB_USER_PASSWORD}'
    params = urllib.parse.quote_plus(connection)
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT =587
    MAIL_USE_TLS =True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    