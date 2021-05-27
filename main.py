import datetime

from flask import Flask
from mongoengine import *
import json
from bson import ObjectId
import sys

app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



class Item(Document):
    product_name = StringField(required=True, max_length=40)
    product_price = IntField(required=True)
    date = DateTimeField(default=datetime.datetime.now())



@app.route('/')
@app.route('/get', methods=['GET'])
def get_list():
    output = {'list': []}
    price_sum = 0
    for it in Item.objects:
        single_item = {"id": it.id,
                       "product_name": it.product_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output['list'].append(single_item)
        price_sum += single_item['product_price']
    output['sum'] = price_sum
    return JSONEncoder().encode(output)


@app.route('/get/<spend_id>', methods=['GET'])
def get_one(spend_id):
    output = {'list': [], 'sum': 0}
    for it in Item.objects(id=spend_id):
        output = {'list': [{"id": it.id,
                            "product_name": it.product_name,
                            "product_price": it.product_price,
                            "date": str(it.date)}],
                  'sum': it.product_price}
    return JSONEncoder().encode(output)



@app.route('/post/<product_name>/<product_price>', methods=['POST', 'GET'])
def post_one(product_name, product_price):
    Item(product_name=product_name, product_price=product_price).save()
    return "done"


@app.route('/put/<spend_id>/<product_name>/<product_price>', methods=['PUT', 'GET'])
def update(spend_id, product_name, product_price):
    Item.objects(id=spend_id).update_one(set__product_name=product_name, set__product_price=product_price)
    return get_one(spend_id)


@app.route('/delete/<spend_id>', methods=['DELETE'])
def delete(spend_id):
    return sys._getframe().f_code.co_name


if __name__ == '__main__':
    connect('spends_db')
    app.run(debug=True)
    disconnect()
