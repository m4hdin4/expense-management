from app import app
from app.models.Item import Item
from app.models.User import User
from app.models.Category import Category

if __name__ == '__main__':
    Item.drop_collection()
    Category.drop_collection()
    User.drop_collection()
    app.run(debug=True)
