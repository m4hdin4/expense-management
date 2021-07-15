from app.models.Category import Category
from app.models.Item import Item
from app.utils.JSONEncoder import JSONEncoder
from app.utils.serializer.item import *
from mongoengine import Q
from app.controllers.User.user import get_user_by_token
from flask import request, abort, Blueprint
from jsonschema import validate

app_item = Blueprint("item", __name__, url_prefix="/item")


@app_item.route('', methods=['GET'])
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
        abort(401)
    validate(instance=request.args, schema=Get_Item_Schema)
    spend_id = request.args['spend_id']
    user = get_user_by_token(request.headers['token'])
    it = Item.objects(Q(id=spend_id) & Q(user=user)).first()
    if it is None:
        return {}
    output = {'list': [{"id": it.id,
                        "username": it.user.username,
                        "product_name": it.product_name,
                        "category": it.category.category_name,
                        "product_price": it.product_price,
                        "date": str(it.date)}],
              'sum': it.product_price}
    return JSONEncoder().encode(output), 200


@app_item.route('', methods=['POST'])
def insert():
    """
    @api {POST} /item insert item
    @apiName insert
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} product_name
    @apiBody {Number} product_price
    @apiBody {String} category

    @apiSuccess {Object} returns json contains inserted object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 201 CREATED
            {
                "spend_id": "60b4c7da7ba96ba33ab0d978",
                "message": "item added"
            }
    """
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Insert_Item_Schema)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    if category_item is None:
        return JSONEncoder().encode({"error": "category not found"}), 404
    inserted = Item(product_name=product_name, product_price=product_price,
                    category=category_item, user=user).save()
    return JSONEncoder().encode({"spend_id": str(inserted.id), "message": "item added"}), 201


@app_item.route('', methods=['PUT'])
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

    @apiSuccess {Object} returns json contains updated object id

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
            {
                "spend_id": "60b4c7da7ba96ba33ab0d978",
                "message": "item updated"
            }
    """
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Update_Item_Schema)
    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    if Item.objects(Q(id=spend_id) & Q(user=user)).first() is None:
        return JSONEncoder().encode({"error": "item not found"}), 404
    category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    if category_item is None:
        return JSONEncoder().encode({"error": "category not found"}), 404
    Item.objects(Q(id=spend_id) & Q(user=user)).update_one(set__product_name=product_name,
                                                           set__product_price=product_price,
                                                           set__category=category_item)
    return JSONEncoder().encode({"spend_id": spend_id, "error": "item updated"}), 200


@app_item.route('', methods=['DELETE'])
def delete():
    """
    @api {DELETE} /item delete item
    @apiName delete
    @apiGroup item

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} spend_id

    @apiSuccess {Object} returns json contains a message

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
            {
                "message": "DELETED"
            }
    """
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.args, schema=Delete_Item_Schema)
    spend_id = request.args['spend_id']
    query = Item.objects(Q(id=spend_id) & Q(user=user))
    if query.first() is None:
        return JSONEncoder().encode({"error": "item not found"}), 404
    query.delete()
    return JSONEncoder().encode({"message": "DELETED"}), 200
