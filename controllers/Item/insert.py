from main import app
from models.Item import Item
from models.Category import Category
from mongoengine import Q
from controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


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
