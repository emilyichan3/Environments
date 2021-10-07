import urllib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b6dd78c7526a3b11e596a1198c8c12c9737cfac83b0ccd35f8534dccfe45641a'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cooklab.db'

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=LAPTOP-S1BRJEOA\SQLEXPRESS;DATABASE=SAMLTD;UID=sa;PWD=saa")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# officially run the process.
from flaskapp_env import routes 



