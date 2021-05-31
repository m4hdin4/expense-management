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
    """
    @api {UNLOCK} /login log in users account
    @apiName login
    @apiGroup user

    @apiBody {String} username
    @apiBody {String} password

    @apiSuccess {String} returns a token - a unique session id that is valid for each login for 3 hours

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        9d2db59d-5d16-4773-adb1-f39e71321e4f
    """
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
        return 'username or password is wrong', 401


@app.route('/user', methods=['GET'])
def get_list():
    """
    @api {GET} /user get user expenses
    @apiName get_list
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiSuccess {Object} returns query objects if exists

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "list":
            [
                {
                    "id": "60b4c7a37ba96ba33ab0d977",
                    "username": "m4hdin4",
                    "product_name": "test1",
                    "category": "test_category",
                    "product_price": 10000,
                    "date": "2021-05-31 15:54:45.024000"
                },
                {
                    "id": "60b4c7da7ba96ba33ab0d978",
                    "username": "m4hdin4",
                    "product_name": "test1",
                    "category": "test_category",
                    "product_price": 10000,
                    "date": "2021-05-31 15:54:45.024000"
                }
            ],
            "sum": 20000
        }
    """
    if not request.headers or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
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


@app.route('/item', methods=['GET'])
def get_one():
    """
    @api {GET} /item get one item
    @apiName get_one
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

    @apiSuccess {Object} returns the query object if exists

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "list":
            [
                {
                    "id": "60b4c7a37ba96ba33ab0d977",
                    "username": "m4hdin4",
                    "product_name": "test1",
                    "category": "test_category",
                    "product_price": 10000,
                    "date": "2021-05-31 15:54:45.024000"
                }
            ],
            "sum": 10000
        }
    """
    if not request.json or \
            not request.headers or \
            not request.args or \
            'token' not in request.headers or \
            'spend_id' not in request.args:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    spend_id = request.args['spend_id']
    if user is None:
        return 'you should login first', 401
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


@app.route('/category', methods=['GET'])
def get_category():
    """
    @api {GET} /user get category expenses
    @apiName get_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} category

    @apiSuccess {Object} returns query objects if exists

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "list":
            [
                {
                    "id": "60b4c7a37ba96ba33ab0d977",
                    "username": "m4hdin4",
                    "product_name": "test1",
                    "category": "test_category",
                    "product_price": 10000,
                    "date": "2021-05-31 15:54:45.024000"
                },
                {
                    "id": "60b4c7da7ba96ba33ab0d978",
                    "username": "m4hdin4",
                    "product_name": "test1",
                    "category": "test_category",
                    "product_price": 10000,
                    "date": "2021-05-31 15:54:45.024000"
                }
            ],
            "sum": 20000
        }
    """
    if not request.json or \
            not request.headers or \
            not request.args or \
            'token' not in request.headers or \
            'category' not in request.args:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    category = request.args['category']
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


@app.route('/item', methods=['POST'])
def insert():
    """
    @api {POST} /item insert a new expense
    @apiName insert
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category

    @apiSuccess {String} returns inserted object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        60b4c7da7ba96ba33ab0d978
    """
    if not request.json or \
            not request.headers or \
            'product_name' not in request.json or \
            'product_price' not in request.json or \
            'category' not in request.json or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        abort(401)
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


@app.route('/signup', methods=['POST'])
def signup():
    """
    @api {POST} /signup insert a new user
    @apiName signup
    @apiGroup user

    @apiBody {String} username
    @apiBody {String} password

    @apiSuccess {String} returns inserted user id(username)

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        m4hdin4
    """
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        abort(400)
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username).first() is not None:
        abort(401)
    try:
        User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
        return username
    except:
        abort(400)


@app.route('/item', methods=['PUT'])
def update():
    """
    @api {PUT} /item update an available item
    @apiName update
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category
    @apiBody {String} spend_id

    @apiSuccess {String} returns updated object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        60b4c7da7ba96ba33ab0d978
    """
    if not request.json or \
            not request.headers or \
            'product_name' not in request.json or \
            'category' not in request.json or \
            'product_price' not in request.json or \
            'spend_id' not in request.json \
            or 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401

    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    if Item.objects(Q(id=spend_id) & Q(user=user)).first() is None:
        abort(404)
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user))[0]
    except:
        category_item = Category(category_name=category, user=user).save()
    try:
        flag = Item.objects(Q(id=spend_id) & Q(user=user)).update_one(set__product_name=product_name,
                                                                      set__product_price=product_price,
                                                                      set__category=category_item)
        return spend_id
    except:
        abort(400)


@app.route('/category', methods=['PUT'])
def update_category():
    """
    @api {PUT} /category update an available category name
    @apiName update_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} new_category
    @apiBody {String} old_category

    @apiSuccess {String} returns updated category name

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        updated_category
    """
    if not request.json or \
            not request.headers or \
            'old_category' not in request.json or \
            'new_category' not in request.json or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    old_category = request.json['old_category']
    new_category = request.json['new_category']

    flag = Category.objects(Q(category_name=old_category) & Q(user=user)).update_one(set__category_name=new_category)
    if flag == 1:
        return new_category
    else:
        abort(404)


@app.route('/item', methods=['DELETE'])
def delete():
    """
    @api {DELETE} /item delete an available expense
    @apiName delete
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

    @apiSuccess {String} returns text "DELETED"

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        DELETED
    """
    if not request.args or \
            not request.headers or \
            'spend_id' not in request.args or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    spend_id = request.args['spend_id']
    query = Item.objects(Q(id=spend_id) & Q(user=user))
    if query.first() is None:
        abort(404)
    try:
        query.delete()
        return 'DELETED'
    except:
        abort(400)


@app.route('/category', methods=['DELETE'])
def delete_category():
    """
    @api {DELETE} /category delete an available category
    @apiName delete_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} category

    @apiSuccess {String} returns text "DELETED"

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        DELETED
    """
    if not request.args or \
            not request.headers or \
            'category' not in request.args or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    category = request.args['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
        Item.objects(category=category_item).delete()
        category_item.delete()
        return 'DELETED'
    except:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
