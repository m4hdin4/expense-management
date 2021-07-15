from mongoengine import connect
import redis

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
connect('spends_db')

from flask import Flask
from app.controllers.User.user import app_user
from app.controllers.Category.category import app_category
from app.controllers.Item.item import app_item
from app.controllers.controller_exceptions.Exceptions import app_exception

app = Flask(__name__)

app.register_blueprint(app_user)
app.register_blueprint(app_category)
app.register_blueprint(app_item)
app.register_blueprint(app_exception)
