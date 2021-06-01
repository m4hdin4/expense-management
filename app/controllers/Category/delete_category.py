from app import app
from app.models.Item import Item
from app.models.Category import Category
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


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

