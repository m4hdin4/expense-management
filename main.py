# from models.User import User
# from models.Item import Item
# from models.Category import Category

from flask import Flask
from mongoengine import *
import redis


app = Flask(__name__)
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
connect('spends_db')


if __name__ == '__main__':

    # Item.drop_collection()
    # Category.drop_collection()
    # User.drop_collection()
    app.run(debug=True)
