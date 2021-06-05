from app import app
from app.models.Category import Category
from app.models.Item import Item
from app.utils.JSONEncoder import JSONEncoder
from app.utils.serializer.item import *
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort
from jsonschema import validate


@app.route('/item', methods=['GET'])
def get_one():
    """
    @api {GET} /item get item
    @apiName get_one
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

    @apiSuccess {Object} returns the query object if exists

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
                }
            ],
            "sum": 10000
        }
    """
    if not request.headers or 'token' not in request.headers:
        # not request.args or \

        # 'spend_id' not in request.args:
        abort(400)
    try:
        validate(instance=request.args, schema=Get_Item_Schema)
        spend_id = request.args['spend_id']
    except:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    try:
        it = Item.objects(Q(id=spend_id) & Q(user=user)).first()
        output = {'list': [{"id": it.id,
                            "username": it.user.username,
                            "product_name": it.product_name,
                            "category": it.category.category_name,
                            "product_price": it.product_price,
                            "date": str(it.date)}],
                  'sum': it.product_price}
        return JSONEncoder().encode(output), 200
    except:
        return {}


@app.route('/item', methods=['POST'])
def insert():
    """
    @api {POST} /item insert item
    @apiName insert
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category

    @apiSuccess {String} returns inserted object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 201 CREATED
        60b4c7da7ba96ba33ab0d978
    """
    if 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        abort(401)
    try:
        validate(instance=request.json, schema=Insert_Item_Schema)
    except Exception as e:
        print(e)
        abort(400)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user))[0]
    except:
        return "category not found", 404
    try:
        inserted = Item(product_name=product_name, product_price=product_price,
                        category=category_item, user=user).save()
        return str(inserted.id), 201
    except:
        abort(400)


@app.route('/item', methods=['PUT'])
def update():
    """
    @api {PUT} /item update item
    @apiName update
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category
    @apiBody {String} spend_id

    @apiSuccess {String} returns updated object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        60b4c7da7ba96ba33ab0d978
    """
    if 'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    try:
        validate(instance=request.json, schema=Update_Item_Schema)
    except:
        abort(400)
    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    if Item.objects(Q(id=spend_id) & Q(user=user)).first() is None:
        abort(404)
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user))[0]
    except:
        category_item = Category(category_name=category, user=user).save()
    try:
        Item.objects(Q(id=spend_id) & Q(user=user)).update_one(set__product_name=product_name,
                                                               set__product_price=product_price,
                                                               set__category=category_item)
        return spend_id
    except:
        abort(400)


@app.route('/item', methods=['DELETE'])
def delete():
    """
    @api {DELETE} /item delete item
    @apiName delete
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

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
        validate(instance=request.args, schema=Delete_Item_Schema)
    except:
        abort(400)
    spend_id = request.args['spend_id']
    query = Item.objects(Q(id=spend_id) & Q(user=user))
    if query.first() is None:
        abort(404)
    try:
        query.delete()
        return 'DELETED'
    except:
        abort(400)
