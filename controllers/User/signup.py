from main import app
from models.User import User
import hashlib
from flask import request, abort


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
        return "user exists", 403
    try:
        User(username=username, password=str(hashlib.md5(password.encode()).hexdigest())).save()
        return username
    except:
        abort(400)