from app import app
from app.models.Category import Category
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


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

