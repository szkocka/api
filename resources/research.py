from flask.ext.restful import Resource

class Research(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, research_id):
        return research_id

    def put(self, research_id):
        return research_id
