from main import redisClient
from models.User import User


def get_user_by_token(token):
    try:
        username = redisClient.get(token).decode("utf-8")
        user = User.objects(username=username).first()
        return user
    except:
        return None