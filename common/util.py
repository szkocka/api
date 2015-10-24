import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer
import inspect


class TokenUtil:

    def __init__(self):
        self.serializer = None

    def __init_serializer(self, secret_key):
        self.serializer = TokenSerializer(secret_key, expires_in=36000)

    def generate(self, user_id, secret_key):
        if not self.serializer:
            self.__init_serializer(secret_key)

        return self.serializer.dumps(str(user_id))

    def verify(self, token, secret_key):
        if not self.serializer:
            self.__init_serializer(secret_key)

        return self.serializer.loads(token)


def hash_password(password):
    return hashlib.sha256(password).hexdigest()


def im_self(func):
    if inspect.ismethod(func):
        return func.im_self
    else:
        closures = func.func_closure
        method = closures[-1].cell_contents
        return im_self(method)
