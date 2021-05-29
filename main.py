import datetime
from flask import Flask
from flask import request
from flask import abort
from mongoengine import *
import json
from bson import ObjectId

app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Category(Document):
    category_name = StringField(required=True, max_length=40, unique=True)


class Item(Document):
    product_name = StringField(required=True, max_length=40)
    category = ReferenceField(Category, required=True)
    product_price = IntField(required=True)
    date = DateTimeField(default=datetime.datetime.now())


@app.route('/')
@app.route('/get', methods=['GET'])
def get_list():
    output_list = []
    for it in Item.objects:
        single_item = {"id": it.id,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = Item.objects.sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/get/<spend_id>', methods=['GET'])
def get_one(spend_id):
    try:
        it = Item.objects(id=spend_id).first()
        output = {'list': [{"id": it.id,
                            "product_name": it.product_name,
                            "category": it.category.category_name,
                            "product_price": it.product_price,
                            "date": str(it.date)}],
                  'sum': it.product_price}
        return JSONEncoder().encode(output), 200
    except:
        abort(404)


@app.route('/get/category/<category>', methods=['GET'])
def get_category(category):
    category_item = Category.objects(category_name=category).first()
    output_list = []
    for it in Item.objects(category=category_item):
        single_item = {"id": it.id,
                       "product_name": it.product_name,
                       "category": it.category.category_name,
                       "product_price": it.product_price,
                       "date": str(it.date)}
        output_list.append(single_item)
    output_sum = Item.objects(category=category_item).sum('product_price')
    output = {'list': output_list, 'sum': output_sum}
    return JSONEncoder().encode(output), 200


@app.route('/post', methods=['POST'])
def insert():
    if not request.json or \
            'product_name' not in request.json or \
            'product_price' not in request.json or \
            'category' not in request.json:
        abort(400)
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category)[0]
        print("ok")
    except:
        category_item = Category(category_name=category).save()
    try:
        inserted = Item(product_name=product_name, product_price=product_price, category=category_item).save()
        return get_one(inserted.id)
    except:
        abort(400)


@app.route('/put', methods=['PUT'])
def update():
    if not request.json or 'product_name' not in request.json or \
            'category' not in request.json or \
            'product_price' not in request.json or \
            'spend_id' not in request.json:
        abort(400)
    spend_id = request.json['spend_id']
    product_name = request.json['product_name']
    product_price = request.json['product_price']
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category).first()
    except:
        category_item = Category(category_name=category).save()
    try:
        Item.objects(id=spend_id)[0]
    except:
        abort(404)
    try:
        Item.objects(id=spend_id).update_one(set__product_name=product_name,
                                             set__product_price=product_price,
                                             set__category=category_item)
        return get_one(spend_id)
    except:
        abort(400)


@app.route('/put/category', methods=['PUT'])
def update_category():
    if not request.json or 'old_category' not in request.json or \
            'new_category' not in request.json:
        abort(400)
    old_category = request.json['old_category']
    new_category = request.json['new_category']

    flag = Category.objects(category_name=old_category).update(category_name=new_category)
    if flag == 1:
        return get_category(new_category)
    else:
        abort(404)


@app.route('/delete', methods=['DELETE'])
def delete():
    if not request.json or 'spend_id' not in request.json:
        abort(400)
    spend_id = request.json['spend_id']
    try:
        Item.objects(id=spend_id).delete()
        return 'DELETED'
    except:
        abort(404)


@app.route('/delete/category', methods=['DELETE'])
def delete_category():
    if not request.json or 'category' not in request.json:
        abort(400)
    category = request.json['category']
    try:
        category_item = Category.objects(category_name=category).first()
        Item.objects(category=category_item).delete()
        category_item.delete()
        return 'DELETED'
    except:
        abort(404)


if __name__ == '__main__':
    connect('spends_db')
    app.run(debug=True)
    disconnect()
