from flask.ext.restful import Resource
from common.util import handle_object_id


class Research(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.researches = self.db['researches']

    def get(self, research_id):
        def get_research():
            research = self.researches.find_one({'_id': research_id})

            if research is None:
                return {'message': 'Research with ID: {0} not found.'.format(research_id)}, 404

            return handle_object_id(research), 200

        return get_research()

    def put(self, research_id):
        return research_id
