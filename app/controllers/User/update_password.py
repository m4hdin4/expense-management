from app import app
from app.models.User import User
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
import hashlib


@app.route('/user', methods=['PUT'])
def update_password():
    """
    @api {PUT} /user update the user password
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

