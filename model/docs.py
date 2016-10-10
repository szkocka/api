import logging
import os

from google.appengine.api import search
from model.db import Research, StatusType

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
        page_size = int(os.environ['PAGE_SIZE'])
        offset = page_size * int(page)

        query = 'title:*'
        if keyword:
            query = keyword.encode('utf-8').strip()

        if status:
            query += ' AND status:{0}'.format(status)
        if tag:
            encoded_tag = tag.encode('utf-8').strip()
            query += ' AND tags:{0}'.format(encoded_tag)

        search_query = search.Query(
                query_string=query.strip(),
                options=search.QueryOptions(ids_only=True,
                                            limit=page_size,
                                            offset=offset)
        )

        logging.info(query)
        results = RESEARCH_INDEX.search(search_query).results

        found_researches = map(lambda r: Research.get(int(r.doc_id)), results)

        return filter(lambda r: r.status != StatusType.DELETED, found_researches)
