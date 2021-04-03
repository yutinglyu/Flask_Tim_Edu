import os


class Config:
    SECRET_KEY = "7abc939cc7882fc9740f0435bd38fd67"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.163.com'
    # 163:Non SSL:25/  SSL:465/994
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_USERNAME = 'yutinglv1994@163.com'
    # MAIL_PASSWORD = 'VGRJTOGLHDMZHEZN'
