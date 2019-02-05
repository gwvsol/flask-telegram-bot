from flask import Flask, abort, jsonify, make_response, request
from rethinkdbcm import UseDatabase
from hashlib import md5
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def setpasswd(login: str, passw: str) -> str:
    """Преобразование пароля и логина в хеш MD5"""
    return str(md5(str(passw+login).lower().encode('utf-8')).hexdigest())




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
