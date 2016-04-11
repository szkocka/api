from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()
    hashed_password = ndb.StringProperty()
    cv = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_email(cls, email):
        ls = cls.query(User.email == email).fetch()
        if len(ls) > 0:
            return ls[0]
        else:
            return None

    @classmethod
    def by_email_and_password(cls, email, password):
        ls = cls.query(
                cls.email == email,
                cls.hashed_password == password).fetch()
        if len(ls) > 0:
            return ls[0]
        else:
            return None

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
    def all(cls):
        return cls.query().fetch()

    @classmethod
    def by_supervisor(cls, user_key):
        return cls.query(cls.supervisor_key == user_key).fetch()

    @classmethod
    def by_researcher(cls, user_key):
        return cls.query(cls.researchers_keys == user_key).fetch()


class ResearchInvite(ndb.Model):
    research_key = ndb.KeyProperty(kind=Research)
    email = ndb.StringProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_email(cls, email):
        return cls.query(cls.email == email).fetch()


class Forum(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    research_key = ndb.KeyProperty(kind=Research)
    subject = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_research(cls, research_key):
        return cls.query(cls.research_key == research_key).fetch()


class Message(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    forum_key = ndb.KeyProperty(kind=Forum)
    text = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def by_forum(cls, forum_key):
        return cls.query(cls.forum_key == forum_key).fetch()


class News(ndb.Model):
    creator_key = ndb.KeyProperty(kind=User)
    title = ndb.TextProperty()
    body = ndb.TextProperty()
    image_url = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def all(cls):
        return cls.query().order(-cls.creation_time)


class AboutPage(ndb.Model):
    content = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    last_update_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)
