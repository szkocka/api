from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()
    hashed_password = ndb.StringProperty()

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def by_email(cls, email):
        return cls.query(User.email == email)

    @classmethod
    def by_email_and_password(cls, email, password):
        return cls.query(cls.email == email,
                         cls.hashed_password == password)

    def is_supervisor_of(self, research):
        return self.id == research.supervisor.id

    def is_researcher_of(self, research):
        return research in set(self.researches)


class Research(ndb.Model):
    supervisor_id = ndb.KeyProperty(kind=User)
    title = ndb.TextProperty()
    area = ndb.StringProperty()
    status = ndb.StringProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    brief_desc = ndb.TextProperty()
    detailed_desc = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    image_url = ndb.StringProperty()
    researchers = ndb.KeyProperty(kind=User, repeated=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)

    @classmethod
    def all(cls):
        return cls.query().fetch(100)


class InvitedResearcher(ndb.Model):
    research_id = ndb.KeyProperty(kind='Research')
    email = ndb.StringProperty()

    @classmethod
    def by_email(cls, email):
        return cls.query(cls.email == email)


class Forum(ndb.Model):
    creator_id = ndb.KeyProperty(kind='User')
    research_id = ndb.KeyProperty(kind='Research')
    subject = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get(cls, _id):
        return cls.get_by_id(_id)


class Message(ndb.Model):
    creator_id = ndb.KeyProperty(kind='User')
    forum_id = ndb.KeyProperty(kind='Forum')
    message = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)


class News(ndb.Model):
    creator_id = ndb.KeyProperty(kind='User')
    title = ndb.TextProperty()
    body = ndb.TextProperty()
    creation_time = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def all(cls):
        return cls.query().order(-cls.creation_time)
