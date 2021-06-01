from app import app
from app.models.Item import Item
from app.models.Category import Category
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
from app.utils.JSONEncoder import JSONEncoder


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
    if not request.headers or \
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
