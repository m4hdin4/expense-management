from app import app
from app.models.Category import Category
from app.models.Item import Item
from app.models.User import User
from app.utils.JSONEncoder import JSONEncoder
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
import hashlib


@app.route('/user', methods=['GET'])
def get_list():
    """
    @api {GET} /user get user list
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


@app.route('/user', methods=['PUT'])
def update_password():
    """
    @api {PUT} /user update user password
    @apiName update_password
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} new_password
    @apiBody {String} old_password

    @apiSuccess {String} returns username

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        m4hdin4
    """
    if not request.json or \
            not request.headers or \
            'old_password' not in request.json or \
            'new_password' not in request.json or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    old_password = request.json['old_password']
    new_password = request.json['new_password']
    if user.password != str(hashlib.md5(old_password.encode()).hexdigest()):
        return 'password is not correct', 401
    try:
        User.objects(username=user.username).update_one(set__password=str(hashlib.md5(new_password.encode()).hexdigest()))
        return user.username
    except:
        abort(400)


@app.route('/user', methods=['DELETE'])
def delete_account():
    """
    @api {DELETE} /user delete account
    @apiName delete_account
    @apiGroup user

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} password

    @apiSuccess {String} returns text "DELETED"

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        DELETED
    """
    if not request.json or \
            not request.headers or \
            'password' not in request.json or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    password = request.json['password']
    if user.password != str(hashlib.md5(password.encode()).hexdigest()):
        return 'password is not correct', 401
    query = Category.objects(user=user)
    for category in query:
        Item.objects(category=category).delete()
        category.delete()
    user.delete()
    return 'DELETED', 200
