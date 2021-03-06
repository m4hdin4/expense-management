from app.models.Item import Item
from app.models.Category import Category
from app.utils.serializer.category import *
from mongoengine import Q
from app.controllers.User.user import get_user_by_token
from flask import request, abort, Blueprint
from app.utils.JSONEncoder import JSONEncoder
from jsonschema import validate

app_category = Blueprint("category", __name__, url_prefix="/category")


@app_category.route('', methods=['POST'])
def insert_category():
    """
    @api {POST} /category insert category
    @apiName insert_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} category

    @apiSuccess {Object} returns json contains category name

    @apiSuccessExample Success-Response:
        HTTP/1.1 201 CREATED
            {
                "category": "test_category1",
                "message": "category added"
            }
    """
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Insert_Category_Schema)
    category = request.json['category']
    Category(category_name=category, user=user).save()
    return JSONEncoder().encode({"category": category, "message": "category added"}), 201


@app_category.route('', methods=['GET'])
def get_category():
    """
    @api {GET} /user get category
    @apiName get_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} category
    @apiParam {String} page_size string of numbers to show how much item should be per page
    @apiParam {String} page_num string of numbers to show which page you want

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
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.args, schema=Get_Category_Schema)
    category = request.args['category']
    page_size = int(request.args['page_size']) or 20
    page_num = int(request.args['page_num']) or 1
    offset = (page_num - 1) * page_size
    category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    output_list = []
    query = Item.objects(Q(category=category_item)).skip(offset).limit(page_size)
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


@app_category.route('', methods=['PUT'])
def update_category():
    """
    @api {PUT} /category update category
    @apiName update_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiBody {String} new_category
    @apiBody {String} old_category

    @apiSuccess {Object} returns json contains updated category name

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
            {
                "category_name": "updated_category"
            }
    """
    if 'token' not in request.headers:
        abort(401)
    user = get_user_by_token(request.headers['token'])
    validate(instance=request.json, schema=Update_Category_Schema)
    old_category = request.json['old_category']
    new_category = request.json['new_category']

    flag = Category.objects(Q(category_name=old_category) & Q(user=user)).update_one(set__category_name=new_category)
    if flag == 1:
        return JSONEncoder().encode({"category_name": new_category}), 200
    else:
        return JSONEncoder().encode({"error": "category not found"}), 404


@app_category.route('', methods=['DELETE'])
def delete_category():
    """
    @api {DELETE} /category delete category
    @apiName delete_category
    @apiGroup category

    @apiHeader {String} token - a unique session id that is valid for each login for 3 hours

    @apiParam {String} category

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
    validate(instance=request.args, schema=Delete_Category_Schema)
    category = request.args['category']
    category_item = Category.objects(Q(category_name=category) & Q(user=user)).first()
    if category_item is None:
        return JSONEncoder().encode({"error": "category not found"}), 404
    Item.objects(category=category_item).delete()
    category_item.delete()
    return JSONEncoder().encode({"message": "DELETED"}), 200
