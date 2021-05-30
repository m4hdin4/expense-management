import datetime
from flask import Flask
from flask import request
from flask import abort
from mongoengine import *
from mongoengine.queryset.visitor import Q
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
    user = ReferenceField(User, required=True)
    category_name = StringField(max_length=40, unique_with='user')


class Item(Document):
    user = ReferenceField(User, required=True)
    product_name = StringField(required=True, max_length=40)
    category = ReferenceField(Category, required=True)
    product_price = IntField(required=True)
    date = DateTimeField(default=datetime.datetime.now())


def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user
    except:
        return None


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
        redisClient.set(token, username)
        redisClient.expire(token, timedelta(hours=3))
        return token, 200
    except:
        return 'username or password is wrong', 403


@app.route('/', methods=['GET'])
@app.route('/get', methods=['GET'])
def get_list():
    if not request.json or 'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    output_list = []
    query = Item.objects(user=user)
    for it in query:
        single_item = {"id": it.id,
                       "username": it.user.username,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = query.sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/get/<spend_id>', methods=['GET'])
def get_one(spend_id):
    if not request.json or 'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    try:
        it = Item.objects(Q(id=spend_id) & Q(user=user)).first()
        output = {'list': [{"id": it.id,
                            "username": it.user.username,
                            "product_name": it.product_name,
                            "category": it.category.category_name,
                            "product_price": it.product_price,
                            "date": str(it.date)}],
                  'sum': it.product_price}
        return JSONEncoder().encode(output), 200
    except:
        return {}


@app.route('/get/category/<category>', methods=['GET'])
def get_category(category):
    if not request.json or 'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    output_list = []
    query = Item.objects(Q(category=category_item))
    for it in query:
        single_item = {"id": it.id,
                       "username": it.user.username,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = query.sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/post', methods=['POST'])
def insert():
    if not request.json or \
            'product_name' not in request.json or \
            'product_price' not in request.json or \
            'category' not in request.json or \
            'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        abort(403)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user))[0]
    except:
        category_item = Category(category_name=category, user=user).save()
    try:
        inserted = Item(product_name=product_name, product_price=product_price,
                        category=category_item, user=user).save()
        return str(inserted.id)
    except:
        abort(400)


@app.route('/post/user', methods=['POST'])
def signup():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username).first() is not None:
        abort(403)
    try:
        User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
        return username
    except:
        abort(400)


@app.route('/put', methods=['PUT'])
def update():
    if not request.json or 'product_name' not in request.json or \
            'category' not in request.json or \
            'product_price' not in request.json or \
            'spend_id' not in request.json \
            or 'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403

    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    if Item.objects(Q(id=spend_id) & Q(user=user)).first() is None:
        abort(404)
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    except:
        category_item = Category(category_name=category, user=user).save()
    try:
        flag = Item.objects(Q(id=spend_id) & Q(user=user)).update_one(set__product_name=product_name,
                                                                      set__product_price=product_price,
                                                                      set__category=category_item)
        return spend_id
    except:
        abort(400)



@app.route('/put/category', methods=['PUT'])
def update_category():
    if not request.json or 'old_category' not in request.json or \
            'new_category' not in request.json or \
            'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    old_category = request.json['old_category']
    new_category = request.json['new_category']

    flag = Category.objects(Q(category_name=old_category) & Q(user=user)).update(category_name=new_category)
    if flag == 1:
        return get_category(new_category)
    else:
        abort(404)


@app.route('/delete', methods=['DELETE'])
def delete():
    if not request.json or \
            'spend_id' not in request.json or \
            'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    spend_id = request.json['spend_id']
    query = Item.objects(Q(id=spend_id) & Q(user=user))
    if query.first() is None:
        abort(404)
    try:
        query.delete()
        return 'DELETED'
    except:
        abort(400)


@app.route('/delete/category', methods=['DELETE'])
def delete_category():
    if not request.json or \
            'category' not in request.json or \
            'token' not in request.json:
        abort(400)
    user = get_user_by_token(request.json['token'])
    if user is None:
        return 'you should login first', 403
    category = request.json['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
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
