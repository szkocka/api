import logging
import os

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb


class StatusType:
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'
    BANNED = 'BANNED'


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()
    hashed_password = ndb.StringProperty()
    cv = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)
    status = ndb.StringProperty()
    supervisor_in = ndb.IntegerProperty(default=0)
    researcher_in = ndb.IntegerProperty(default=0)
    created_forums = ndb.IntegerProperty(default=0)
    posted_messages = ndb.IntegerProperty(default=0)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_email(cls, email):
        ls = cls.query(
                User.email == email,
                User.status == StatusType.ACTIVE
        ).fetch()
        if len(ls) > 0:
            return ls[0]
        else:
            return None

    @classmethod
    def by_email_and_password(cls, email, password):
        ls = cls.query(
                User.email == email,
                User.hashed_password == password,
                User.status == StatusType.ACTIVE).fetch()
        if len(ls) > 0:
            return ls[0]
        else:
            return None

    @classmethod
    def find_all(cls, cursor, keyword):
        page_size = int(os.environ['PAGE_SIZE'])

        q = cls.query(cls.status.IN([StatusType.ACTIVE, StatusType.BANNED])) \

        if keyword:
            q = q.filter(cls.email >= keyword)
            q = q.filter(cls.email < keyword + u'\ufffd')

        q = q.order(cls.email, cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return q.fetch_page(page_size, start_cursor=cursor_obj)
        return q.fetch_page(page_size)

    def is_supervisor_of(self, research):
        return self.key == research.supervisor_key

    def is_researcher_of(self, research):
        return self.key in set(research.researchers_keys)


class Research(ndb.Model):
    supervisor_key = ndb.KeyProperty(kind=User)
    title = ndb.TextProperty()
    area = ndb.StringProperty()
    status = ndb.StringProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)
    brief_desc = ndb.TextProperty()
    detailed_desc = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    image_url = ndb.StringProperty()
    researchers_keys = ndb.KeyProperty(kind=User, repeated=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def all(cls, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        q = cls.query(cls.status.IN([StatusType.ACTIVE, StatusType.BANNED]))\
            .order(cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return q.fetch_page(page_size, start_cursor=cursor_obj)
        return q.fetch_page(page_size)

    @classmethod
    def all2(cls):
        return cls.query().fetch()

    @classmethod
    def all_tags(cls):
        researches = cls.query().fetch(projection=['tags'])
        tags = set({})
        for r in researches:
            tags.update(r.tags)

        return list(tags)

    @classmethod
    def by_user(cls, user_key, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        q = cls.query(ndb.OR(
                cls.supervisor_key == user_key,
                cls.researchers_keys == user_key),
                cls.status.IN([StatusType.ACTIVE, StatusType.BANNED]))\
            .order(cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return q.fetch_page(page_size, start_cursor=cursor_obj)
        return q.fetch_page(page_size)

    @classmethod
    def by_supervisor(cls, user_key):
        return cls.query(
                cls.supervisor_key == user_key,
                cls.status.IN([StatusType.ACTIVE, StatusType.BANNED]))\
            .fetch()

    @classmethod
    def by_researcher(cls, user_key):
        return cls.query(
                cls.researchers_keys == user_key,
                cls.status.IN([StatusType.ACTIVE, StatusType.BANNED]))\
            .fetch()


class RelationshipType:
    NONE = 'NONE'
    INVITED = 'INVITED'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    WANTS_TO_JOIN = 'WANTS_TO_JOIN'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    SUPERVISOR = 'SUPERVISOR'
    ADDED_BY_ADMIN = 'ADDED_BY_ADMIN'


class ResearchRelationship(ndb.Model):
    research_key = ndb.KeyProperty(kind=Research)
    user_email = ndb.StringProperty()
    type = ndb.StringProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get(cls, research_key, email):
        return cls.query(
                cls.research_key == research_key,
                cls.user_email == email).get()

    @classmethod
    def by_email_and_type(cls, email, type):
        return cls.query(
                cls.type == type,
                cls.user_email == email).fetch()

    @classmethod
    def by_email(cls, email):
        return cls.query(cls.user_email == email).fetch()

    @classmethod
    def by_research_and_type(cls, research_key, type):
        return cls.query(
                cls.type == type,
                cls.research_key == research_key).fetch()


class Forum(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    research_key = ndb.KeyProperty(kind=Research)
    subject = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)
    status = ndb.StringProperty()

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_research(cls, research_key, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        query = cls.query(
                cls.status == StatusType.ACTIVE,
                cls.research_key == research_key)\
            .order(-cls.creation_time, cls.status, cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return query.fetch_page(page_size, start_cursor=cursor_obj)
        return query.fetch_page(page_size)

    @classmethod
    def by_research2(cls, research_key):
        return cls.query(
                cls.status == StatusType.ACTIVE,
                cls.research_key == research_key)\
            .fetch()

    @classmethod
    def by_creator(cls, user_key, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        query = cls.query(
                cls.status == StatusType.ACTIVE,
                cls.creator_key == user_key).order(cls.status, cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return query.fetch_page(page_size, start_cursor=cursor_obj)
        return query.fetch_page(page_size)

    @classmethod
    def by_creator2(cls, user_key):
        query = cls.query(
                cls.status != StatusType.DELETED,
                cls.creator_key == user_key).order(cls.status, cls.key)

        return query.fetch()


class Message(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    forum_key = ndb.KeyProperty(kind=Forum)
    text = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)
    status = ndb.StringProperty()

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_forum(cls, forum_key, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        query = cls.query(
                cls.status == StatusType.ACTIVE,
                cls.forum_key == forum_key)\
            .order(cls.creation_time, cls.status, cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return query.fetch_page(page_size, start_cursor=cursor_obj)
        return query.fetch_page(page_size)

    @classmethod
    def by_forum2(cls, forum_key):
        return cls.query(
                cls.status == StatusType.ACTIVE,
                cls.forum_key == forum_key)\
            .fetch()

    @classmethod
    def by_creator(cls, user_key, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        query = cls.query(
                cls.status == StatusType.ACTIVE,
                cls.creator_key == user_key)\
            .order(cls.creation_time, cls.status, cls.key)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return query.fetch_page(page_size, start_cursor=cursor_obj)
        return query.fetch_page(page_size)

    @classmethod
    def by_creator2(cls, user_key):
        query = cls.query(
                cls.status.IN([StatusType.ACTIVE, StatusType.BANNED]),
                cls.creator_key == user_key)

        return query.fetch()


class News(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    title = ndb.TextProperty()
    body = ndb.TextProperty()
    image_url = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def all(cls, cursor):
        page_size = int(os.environ['PAGE_SIZE'])
        query = cls.query().order(-cls.creation_time)

        if cursor:
            cursor_obj = Cursor.from_websafe_string(cursor)
            return query.fetch_page(page_size, start_cursor=cursor_obj)
        return query.fetch_page(page_size)


class AboutPage(ndb.Model):
    content = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)


class ChangePasswordRequest(ndb.Model):
    user_key = ndb.KeyProperty(kind=User)
    token = ndb.StringProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def by_token(cls, token):
        ls = cls.query(cls.token == token).fetch()
        if len(ls) > 0:
            return ls[0]
        else:
            return None
