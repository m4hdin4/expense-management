import datetime
from flask import Flask
from flask import request
from flask import abort
from mongoengine import *
import redis
import json
from bson import ObjectId
from datetime import timedelta
import uuid
import hashlib

app = Flask(__name__)
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
connect('spends_db')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class User(Document):
    username = StringField(primary_key=True, max_length=40)
    password = StringField(required=True)


class Category(Document):
    category_name = StringField(primary_key=True, max_length=40)


class Item(Document):
    user = ReferenceField(User, required=True)
    product_name = StringField(required=True, max_length=40)
    category = ReferenceField(Category, required=True)
    product_price = IntField(required=True)
    date = DateTimeField(default=datetime.datetime.now())


def get_user_by_token(token):
    pass


@app.route('/login', methods=['UNLOCK'])
def login():
    if not request.json or \
            'username' not in request.json or \
            'password' not in request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    try:
        user = User.objects(username=username, password=str(hashlib.md5(password.encode()).hexdigest()))[0]
        token = str(uuid.uuid4())
        redisClient.set(token, user.id)
        redisClient.expire(token, timedelta(hours=3))
        return token, 200
    except:
        return 'username or password is wrong', 403


@app.route('/', methods=['GET'])
@app.route('/get', methods=['GET'])
def get_list():
    output_list = []
    for it in Item.objects:
        single_item = {"id": it.id,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = Item.objects.sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/get/<spend_id>', methods=['GET'])
def get_one(spend_id):
    try:
        it = Item.objects(id=spend_id).first()
        output = {'list': [{"id": it.id,
                            "product_name": it.product_name,
                            "category": it.category.category_name,
                            "product_price": it.product_price,
                            "date": str(it.date)}],
                  'sum': it.product_price}
        return JSONEncoder().encode(output), 200
    except:
        abort(404)


@app.route('/get/category/<category>', methods=['GET'])
def get_category(category):
    category_item = Category.objects(category_name=category).first()
    output_list = []
    for it in Item.objects(category=category_item):
        single_item = {"id": it.id,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = Item.objects(category=category_item).sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/post', methods=['POST'])
def insert():
    if not request.json or \
            'product_name' not in request.json or \
            'product_price' not in request.json or \
            'category' not in request.json:
        abort(400)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category)[0]
    except:
        category_item = Category(category_name=category).save()
    try:
        inserted = Item(product_name=product_name, product_price=product_price, category=category_item).save()
        return inserted.id
    except:
        abort(400)


@app.route('/post/user', methods=['POST'])
def insert_user():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username).first() is not None:
        abort(403)
    try:
        user = User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
        return user.id
    except:
        abort(400)


@app.route('/put', methods=['PUT'])
def update():
    if not request.json or 'product_name' not in request.json or \
            'category' not in request.json or \
            'product_price' not in request.json or \
            'spend_id' not in request.json:
        abort(400)
    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category).first()
    except:
        category_item = Category(category_name=category).save()
    try:
        Item.objects(id=spend_id)[0]
    except:
        abort(404)
    try:
        Item.objects(id=spend_id).update_one(set__product_name=product_name,
                                             set__product_price=product_price,
                                             set__category=category_item)
        return get_one(spend_id)
    except:
        abort(400)


@app.route('/put/category', methods=['PUT'])
def update_category():
    if not request.json or 'old_category' not in request.json or \
            'new_category' not in request.json:
        abort(400)
    old_category = request.json['old_category']
    new_category = request.json['new_category']

    flag = Category.objects(category_name=old_category).update(category_name=new_category)
    if flag == 1:
        return get_category(new_category)
    else:
        abort(404)


@app.route('/delete', methods=['DELETE'])
def delete():
    if not request.json or 'spend_id' not in request.json:
        abort(400)
    spend_id = request.json['spend_id']
    try:
        Item.objects(id=spend_id).delete()
        return 'DELETED'
    except:
        abort(404)


@app.route('/delete/category', methods=['DELETE'])
def delete_category():
    if not request.json or 'category' not in request.json:
        abort(400)
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category).first()
        Item.objects(category=category_item).delete()
        category_item.delete()
        return 'DELETED'
    except:
        abort(404)


if __name__ == '__main__':
    # Item.drop_collection()
    # Category.drop_collection()
    # User.drop_collection()
    app.run(debug=True)
