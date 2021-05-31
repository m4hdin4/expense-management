from main import app
from models.Item import Item
from models.Category import Category
from mongoengine import Q
from controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


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
        flag = Item.objects(Q(id=spend_id) & Q(user=user)).update_one(set__product_name=product_name,
                                                                      set__product_price=product_price,
                                                                      set__category=category_item)
        return spend_id
    except:
        print("ok")
        abort(400)