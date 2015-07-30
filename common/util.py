import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer

SECRET_KEY = "qwertyuiopasdfghjklzxcvbnm"
TOKEN_SERIALIZER = TimedJSONWebSignatureSerializer(SECRET_KEY)


def new_token(user_id):
    return TOKEN_SERIALIZER.dumps(str(user_id))

def verify_token(token):
    return TOKEN_SERIALIZER.loads(token)

def hash_password(password):
    return hashlib.sha256(password).hexdigest()
