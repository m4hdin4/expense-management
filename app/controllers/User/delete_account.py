from app import app
from app.models.Item import Item
from app.models.Category import Category
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
import hashlib


@app.route('/user', methods=['DELETE'])
def delete_account():
    """
    @api {DELETE} /user delete an account
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
