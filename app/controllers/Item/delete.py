from app import app
from app.models.Item import Item
from mongoengine import Q
from app.controllers.User.get_user_by_token import get_user_by_token
from flask import request, abort


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

