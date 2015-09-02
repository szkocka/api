import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer

SECRET_KEY = "qwertyuiopasdfghjklzxcvbnm"
TOKEN_SERIALIZER = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=36000)


def generate_token(user_id):
    return TOKEN_SERIALIZER.dumps(str(user_id))

def verify_token(token):
    return TOKEN_SERIALIZER.loads(token)

def hash_password(password):
    return hashlib.sha256(password).hexdigest()

def is_supervisor(current_user, research):
    return current_user.id() == research['supervisor']
