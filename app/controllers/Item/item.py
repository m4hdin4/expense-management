from app import app
from app.models.Category import Category
from app.models.Item import Item
from app.utils.JSONEncoder import JSONEncoder
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


@app.route('/item', methods=['GET'])
def get_one():
    """
    @api {GET} /item get one item
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
    if not request.headers or \
            not request.args or \
            'token' not in request.headers or \
            'spend_id' not in request.args:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    spend_id = request.args['spend_id']
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
    @api {POST} /item insert a new expense
    @apiName insert
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category

    @apiSuccess {String} returns inserted object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        60b4c7da7ba96ba33ab0d978
    """
    if not request.json or \
            not request.headers or \
            'product_name' not in request.json or \
            'product_price' not in request.json or \
            'category' not in request.json or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        abort(401)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(Q(category_name=category) & Q(user=user))[0]
    except:
        category_item = Category(category_name=category, user=user).save()
    try:
        inserted = Item(product_name=product_name, product_price=product_price,
                        category=category_item, user=user).save()
        return str(inserted.id)
    except:
        abort(400)


@app.route('/item', methods=['PUT'])
def update():
    """
    @api {PUT} /item update an available item
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
    if not request.json or \
            not request.headers or \
            'product_name' not in request.json or \
            'category' not in request.json or \
            'product_price' not in request.json or \
            'spend_id' not in request.json or \
            'token' not in request.headers:
        print("ok2")
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401

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
    @api {DELETE} /item delete an available expense
    @apiName delete
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

    @apiSuccess {String} returns text "DELETED"

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        DELETED
    """
    if not request.args or \
            not request.headers or \
            'spend_id' not in request.args or \
            'token' not in request.headers:
        abort(400)
    user = get_user_by_token(request.headers['token'])
    if user is None:
        return 'you should login first', 401
    spend_id = request.args['spend_id']
    query = Item.objects(Q(id=spend_id) & Q(user=user))
    if query.first() is None:
        abort(404)
    try:
        query.delete()
        return 'DELETED'
    except:
        abort(400)