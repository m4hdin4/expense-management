from app import app
from app.models.Item import Item
from app.models.Category import Category
from app.utils.serializer.category import *
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
from app.utils.JSONEncoder import JSONEncoder
from jsonschema import validate


@app.route('/category', methods=['POST'])
def insert_category():
    """
    @api {POST} /category insert category
    @apiName insert_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} category

    @apiSuccess {String} returns category name

    @apiSuccessExample Success-Response:
        HTTP/1.1 201 CREATED
    """
    if not request.headers or 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    try:
        validate(instance=request.json, schema=Get_Category_Schema)
        category = request.json['category']
    except:
        abort(400)
    else:
        Category(category_name=category, user=user).save()
        return category, 201


@app.route('/category', methods=['GET'])
def get_category():
    """
    @api {GET} /user get category
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
    @api {PUT} /category update category
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
    if 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    try:
        validate(instance=request.json, schema=Update_Category_Schema)
    except Exception as e:
        print(e)
        abort(400)
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
    @api {DELETE} /category delete category
    @apiName delete_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} category

    @apiSuccess {String} returns text "DELETED"

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        DELETED
    """
    if 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    try:
        validate(instance=request.args, schema=Delete_Category_Schema)
    except:
        abort(400)
    category = request.args['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
        Item.objects(category=category_item).delete()
        category_item.delete()
        return 'DELETED'
    except:
        abort(404)
