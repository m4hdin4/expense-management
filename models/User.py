from mongoengine import Document, StringField


class User(Document):
    username = StringField(primary_key=True, max_length=40)
    password = StringField(required=True)
