from app.models.User import User
from app.models.Category import Category
from mongoengine import Document, ReferenceField, StringField, IntField, DateTimeField
from datetime import datetime


class Item(Document):
    user = ReferenceField(User, required=True)
    product_name = StringField(required=True, max_length=40)
    category = ReferenceField(Category, required=True)
    product_price = IntField(required=True)
    date = DateTimeField(default=datetime.now())
