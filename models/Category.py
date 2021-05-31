from models.User import User
from mongoengine import Document, ReferenceField, StringField


class Category(Document):
    user = ReferenceField(User, required=True)
    category_name = StringField(max_length=40, unique_with='user')