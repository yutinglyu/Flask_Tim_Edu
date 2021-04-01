# -*- coding: utf-8 -*-
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = "7abc939cc7882fc9740f0435bd38fd67"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_message = u"只有会员才能查看"
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.163.com'
# 163:Non SSL:25/  SSL:465/994
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_USERNAME'] = 'yutinglv1994@163.com'
# app.config['MAIL_PASSWORD'] = 'VGRJTOGLHDMZHEZN'


mail = Mail(app)

from tim_web_server import routes