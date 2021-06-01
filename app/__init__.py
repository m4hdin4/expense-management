from flask import Flask
from mongoengine import connect
import redis


app = Flask(__name__)
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
connect('spends_db')


from app import controllers, models, utils
