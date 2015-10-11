from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

sql = SQLAlchemy()


researches = sql.Table('research_to_user',
    sql.Column('user_id', sql.Integer, sql.ForeignKey('user.id')),
    sql.Column('research_id', sql.Integer, sql.ForeignKey('research.id'))
)


class User(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column(sql.String(128))
    email = sql.Column(sql.String(128), unique=True)
    is_admin = sql.Column(sql.Boolean())
    hashed_password = sql.Column(sql.String(64))

    forums = sql.relationship('Forum', backref='creator', lazy='dynamic')
    messages = sql.relationship('Message', backref='creator', lazy='dynamic')
    news = sql.relationship('News', backref='creator', lazy='dynamic')
    supervise = sql.relationship('Research', backref='supervisor', lazy='dynamic')
    researches = sql.relationship('Research', secondary=researches, backref=sql.backref('researchers', lazy='dynamic'))

    def __init__(self, name, email, hashed_password):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_admin = False

    def json(self):
        return {
            '_id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'role': 'admin' if self.user.is_admin else 'user'
        }


class Research(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    supervisor_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    title = sql.Column(sql.String(1024))
    area = sql.Column(sql.String(128))
    status = sql.Column(sql.String(64))
    creation_time = sql.Column(sql.DateTime)
    brief_desc = sql.Column(sql.Text)
    detailed_desc = sql.Column(sql.Text)
    tags = sql.Column(sql.String(128))
    image_url = sql.Column(sql.String(1024))

    forums = sql.relationship('Forum', backref='research', lazy='dynamic')

    def __init__(self, supervisor, title, area, tags, brief_desc, detailed_desc, image_url):
        self.supervisor_id = supervisor.id
        self.creation_time = datetime.now()
        self.title = title
        self.tags = str(tags)
        self.area = area
        self.status = 'active'
        self.brief_desc = brief_desc
        self.detailed_desc = detailed_desc
        self.image_url = image_url


class Forum(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    research_id = sql.Column(sql.Integer, sql.ForeignKey('research.id'))
    subject = sql.Column(sql.Text)
    creation_time = sql.Column(sql.DateTime)

    messages = sql.relationship('Message', backref='forum', lazy='dynamic')

    def __init__(self, creator, research, subject):
        self.creator_id = creator.id
        self.research_id = research.id
        self.creation_time = datetime.now()
        self.subject = subject


class Message(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    forum_id = sql.Column(sql.Integer, sql.ForeignKey('forum.id'))
    message = sql.Column(sql.Text)
    creation_time = sql.Column(sql.DateTime)

    def __init__(self, creator, forum, message):
        self.creator_id = creator.id
        self.forum = forum.id
        self.creation_time = datetime.now()
        self.message = message


class News(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    creator_id = sql.Column(sql.Integer, sql.ForeignKey('user.id'))
    title = sql.Column(sql.String(1024))
    body = sql.Column(sql.Text)
    creation_time = sql.Column(sql.DateTime)

    def __init__(self, creator, title, body):
        self.creator_id = creator.id
        self.creation_time = datetime.now()
        self.title = title
        self.body = body
