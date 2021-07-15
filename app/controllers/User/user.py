from app import redisClient
from app.models.Category import Category
from app.models.Item import Item
from app.models.User import User
from app.utils.JSONEncoder import JSONEncoder
from app.utils.serializer.user import *
from flask import request, abort, Blueprint
from datetime import timedelta
import hashlib
import uuid
from jsonschema import validate


app_user = Blueprint("user", __name__, url_prefix="/user")


@app_user.route('/signup', methods=['POST'])
def signup():
    """
    @api {POST} /user/signup signup
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
    validate(instance=request.json, schema=Identification_Schema)
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username).first() is not None:
        return JSONEncoder().encode({"error": "user exists"}), 403
    User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
    return JSONEncoder().encode({"username": username, "message": "user added"}), 201


@app_user.route('/login', methods=['POST'])
def login():
    """
    @api {UNLOCK} /user/login login
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
    validate(instance=request.json, schema=Identification_Schema)
    username = request.json['username']
    password = request.json['password']
    if User.objects(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).first() is None:
        abort(401)
    token = str(uuid.uuid4())
    redisClient.set(token, username)
    redisClient.expire(token, timedelta(hours=3))
    return JSONEncoder().encode({"token": token, "message": "login successful"}), 200


@app_user.route('/user_items', methods=['GET'])
def get_list():
    """
    @api {GET} /user/user_items get user list
    @apiName get_list
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} page_size string of numbers to show how much item should be per page
    @apiParam {String} page_num string of numbers to show which page you want

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
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.args, schema=Get_items)
    page_size = int(request.args['page_size']) or 20
    page_num = int(request.args['page_num']) or 1
    offset = (page_num - 1) * page_size
    output_list = []
    query = Item.objects(user=user).skip(offset).limit(page_size)
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


@app_user.route('', methods=['PUT'])
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
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Password_Change_Schema)
    old_password = request.json['old_password']
    new_password = request.json['new_password']
    if user.password != str(hashlib.md5(old_password.encode()).hexdigest()):
        abort(401)
    User.objects(username=user.username).update_one(
        set__password=str(hashlib.md5(new_password.encode()).hexdigest()))
    return JSONEncoder().encode({"username": user.username, "message": "password changed"}), 200


@app_user.route('', methods=['DELETE'])
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
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Check_Password_Schema)
    password = request.json['password']
    if user.password != str(hashlib.md5(password.encode()).hexdigest()):
        abort(401)
    query = Category.objects(user=user)
    for category in query:
        Item.objects(category=category).delete()
        category.delete()
    user.delete()
    return JSONEncoder().encode({"message": "DELETED"}), 200


def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username)[0]
        return user
    except:
        abort(401)
