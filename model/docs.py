import logging

from google.appengine.api import search
from model.db import Research

RESEARCH_INDEX = search.Index(name='research')


class ResearchIndex:
    def __init__(self, research):
        self.doc_id = str(research.key.id())

        desc = research.brief_desc + ' ' + research.detailed_desc
        fields = [
            search.TextField(name='title', value=research.title),
            search.HtmlField(name='desc', value=desc),
            search.AtomField(name='status', value=research.status),
            search.TextField(name='tags', value=' '.join(research.tags))
        ]

        self.doc = search.Document(doc_id=self.doc_id, fields=fields)

    def put(self):
        RESEARCH_INDEX.put(self.doc)

    def delete(self):
        RESEARCH_INDEX.delete(self.doc_id)

    @classmethod
    def find(cls, keyword, status, tag, page):
        page_size = 2
        offset = page_size * page
        query = 'title:{0} OR desc:{0}'.format(keyword)

        if status:
            query += ' AND status:{0}'.format(status)
        if tag:
            query += ' AND tags:{0}'.format(tag)

        search_query = search.Query(
                query_string=query.strip(),
                options=search.QueryOptions(ids_only=True,
                                            limit=page_size,
                                            offset=offset)
        )

        results = RESEARCH_INDEX.search(search_query).results
        logging.info(results)
        return map(lambda r: Research.get(int(r.doc_id)), results)
