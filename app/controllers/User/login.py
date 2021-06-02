from app import app, redisClient
from app.models.User import User
import uuid
from datetime import timedelta
from flask import request, abort
import hashlib


@app.route('/login', methods=['UNLOCK'])
def login():
    """
    @api {UNLOCK} /login login
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
