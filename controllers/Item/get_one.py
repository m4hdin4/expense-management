from main import app
from models.Item import Item
from utils.JSONEncoder import JSONEncoder
from mongoengine import Q
from controllers.User.get_user_by_token import get_user_by_token
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
