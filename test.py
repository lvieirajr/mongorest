# -*- encoding: UTF-8 -*-

from werkzeug.serving import run_simple

from mongorest.wsgi import WSGIDispatcher
from mongorest.resource import Test


if __name__ == '__main__':
    run_simple('127.0.0.1', 8002, WSGIDispatcher([Test]))
