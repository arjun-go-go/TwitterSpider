import json
from flask import Flask, g
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome to Cookie Pool System</h1>'


def get_conn():
    """
    获取
    :return:
    """
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    获取随机的Cookie
    :return: 随机Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies

@app.route('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
