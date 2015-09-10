import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer
import inspect

SECRET_KEY = "qwertyuiopasdfghjklzxcvbnm"
TOKEN_SERIALIZER = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=36000)


def generate_token(user_id):
    return TOKEN_SERIALIZER.dumps(str(user_id))

def verify_token(token):
    return TOKEN_SERIALIZER.loads(token)

def hash_password(password):
    return hashlib.sha256(password).hexdigest()

def im_self(func):
    if inspect.ismethod(func):
        return func.im_self
    else:
        closures = func.func_closure
        method = closures[-1].cell_contents
        return im_self(method)
