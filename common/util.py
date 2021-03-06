import hashlib
import os

from itsdangerous import TimedJSONWebSignatureSerializer as TokenSerializer
import inspect

from model.db import ResearchRelationship


class TokenUtil:
    def __init__(self):
        seed = os.environ['TOKEN_SEED']
        self.serializer = TokenSerializer(seed, expires_in=36000)

    def generate(self, user_id):
        return self.serializer.dumps(str(user_id))

    def verify(self, token):
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


def get_relationship_types(user):
    relationship_types = {}
    if user:
        relationship = ResearchRelationship.by_email(user.email)
        for r in relationship:
            relationship_types[r.research_key.id()] = r.type

    return relationship_types
