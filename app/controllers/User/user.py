from app import app, redisClient
from app.models.Category import Category
from app.models.Item import Item
from app.models.User import User
from app.utils.JSONEncoder import JSONEncoder
from app.utils.serializer.user import *
from flask import request
from datetime import timedelta
import hashlib
import uuid
from jsonschema import validate
from jsonschema.exceptions import ValidationError


@app.route('/signup', methods=['POST'])
def signup():
    """
    @api {POST} /signup signup
    @apiName signup
    @apiGroup user

    @apiBody {String} username
    @apiBody {String} password

    @apiSuccess {Object} returns json contains username

    @apiSuccessExample Success-Response:
        HTTP/1.1 201 CREATED
            {
                "username": m4hdin4,
                "message": "user added"
            }
    """
    try:
        validate(instance=request.json, schema=Identification_Schema)
    except ValidationError as e:
        return JSONEncoder().encode({"error": e.schema}), 400
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username).first() is not None:
        return JSONEncoder().encode({"message": "user exists"}), 403
    try:
        User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
        return JSONEncoder().encode({"username": username, "message": "user added"}), 201
    except Exception as e:
        return JSONEncoder().encode({"error": str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    """
    @api {UNLOCK} /login login
    @apiName login
    @apiGroup user

    @apiBody {String} username
    @apiBody {String} password

    @apiSuccess {Object} returns json contains a token - a unique session id that is valid for each login for 3 hours

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "token": "9d2db59d-5d16-4773-adb1-f39e71321e4f",
            "message": "login successful"
        }
    """
    try:
        validate(instance=request.json, schema=Identification_Schema)
    except ValidationError as e:
        return JSONEncoder().encode({"error": e.schema}), 400
    username = request.json['username']
    password = request.json['password']
    try:
        user = User.objects(username=username, password=str(hashlib.md5(password.encode()).hexdigest()))[0]
        token = str(uuid.uuid4())
        redisClient.set(token, username)
        redisClient.expire(token, timedelta(hours=3))
        return JSONEncoder().encode({"token": token, "message": "login successful"}), 200
    except:
        return JSONEncoder().encode({"error": "you should login first"}), 401


@app.route('/user_items', methods=['GET'])
def get_list():
    """
    @api {GET} /user_items get user list
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
    if 'token' not in request.headers:
        return JSONEncoder().encode({"error": "authorization failed"}), 400
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return JSONEncoder().encode({"error": "you should login first"}), 401
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


@app.route('/user', methods=['PUT'])
def update_password():
    """
    @api {PUT} /user update user password
    @apiName update_password
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} new_password
    @apiBody {String} old_password

    @apiSuccess {Object} returns json contains username

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
            {
                "username": "m4hdin4",
                "message": "password changed"
            }
    """
    if 'token' not in request.headers:
        return JSONEncoder().encode({"error": "authorization failed"}), 400
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return JSONEncoder().encode({"error": "you should login first"}), 401
    try:
        validate(instance=request.json, schema=Password_Change_Schema)
    except ValidationError as e:
        return JSONEncoder().encode({"error": e.schema}), 400
    old_password = request.json['old_password']
    new_password = request.json['new_password']
    if user.password != str(hashlib.md5(old_password.encode()).hexdigest()):
        return JSONEncoder().encode({"error": "you should login first"}), 401
    try:
        User.objects(username=user.username).update_one(
            set__password=str(hashlib.md5(new_password.encode()).hexdigest()))
        return JSONEncoder().encode({"username": user.username, "message": "password changed"}), 200
    except Exception as e:
        return JSONEncoder().encode({"error": str(e)}), 400


@app.route('/user', methods=['DELETE'])
def delete_account():
    """
    @api {DELETE} /user delete account
    @apiName delete_account
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} password

    @apiSuccess {Object} returns json contains a message

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
            {
                "message": "DELETED"
            }
    """
    if 'token' not in request.headers:
        return JSONEncoder().encode({"error": "authorization failed"}), 400
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return JSONEncoder().encode({"error": "you should login first"}), 401
    try:
        validate(instance=request.json, schema=Check_Password_Schema)
    except ValidationError as e:
        return JSONEncoder().encode({"error": e.schema}), 400
    password = request.json['password']
    if user.password != str(hashlib.md5(password.encode()).hexdigest()):
        return JSONEncoder().encode({"error": "you should login first"}), 401
    query = Category.objects(user=user)
    for category in query:
        Item.objects(category=category).delete()
        category.delete()
    user.delete()
    return JSONEncoder().encode({"message": "DELETED"}), 200


def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user
    except:
        return None
