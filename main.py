from flask import Flask
import sys

app = Flask(__name__)


@app.route('/')
@app.route('/get', methods=['GET'])
def get_list():
    return sys._getframe().f_code.co_name


@app.route('/get/<spend_id>', methods=['GET'])
def get_one(spend_id):
    return sys._getframe().f_code.co_name



@app.route('/post/<product_name>/<product_price>', methods=['POST'])
def post_one(product_name, product_price):
    return sys._getframe().f_code.co_name


@app.route('/put/<spend_id>/<product_name>/<product_price>', methods=['PUT'])
def update(spend_id, product_name, product_price):
    return sys._getframe().f_code.co_name


@app.route('/delete/<spend_id>', methods=['DELETE'])
def delete(spend_id):
    return sys._getframe().f_code.co_name


if __name__ == '__main__':
    app.run(debug=True)
