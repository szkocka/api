from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


researches = db.Table('research_to_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('research_id', db.Integer, db.ForeignKey('research.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    is_admin = db.Column(db.Boolean())
    hashed_password = db.Column(db.String(64))

    forums = db.relationship('Forum', backref='creator', lazy='dynamic')
    messages = db.relationship('Message', backref='creator', lazy='dynamic')
    news = db.relationship('News', backref='creator', lazy='dynamic')
    supervise = db.relationship('Research', backref='supervisor', lazy='dynamic')
    researches = db.relationship('Research', secondary=researches, backref=db.backref('researchers', lazy='dynamic'))

    def __init__(self, name, email, hashed_password):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_admin = False


class Research(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1024))
    area = db.Column(db.String(128))
    status = db.Column(db.String(64))
    creation_time = db.Column(db.DateTime)
    brief_desc = db.Column(db.Text)
    detailed_desc = db.Column(db.Text)
    tags = db.Column(db.String(128))
    image_url = db.Column(db.String(1024))

    forums = db.relationship('Forum', backref='research', lazy='dynamic')

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


class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('research.id'))
    subject = db.Column(db.Text)
    creation_time = db.Column(db.DateTime)

    messages = db.relationship('Message', backref='forum', lazy='dynamic')

    def __init__(self, creator, research, subject):
        self.creator_id = creator.id
        self.research_id = research.id
        self.creation_time = datetime.now()
        self.subject = subject


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))
    message = db.Column(db.Text)
    creation_time = db.Column(db.DateTime)

    def __init__(self, creator, forum, message):
        self.creator_id = creator.id
        self.forum = forum.id
        self.creation_time = datetime.now()
        self.message = message


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1024))
    body = db.Column(db.Text)
    creation_time = db.Column(db.DateTime)

    def __init__(self, creator, title, body):
        self.creator_id = creator.id
        self.creation_time = datetime.now()
        self.title = title
        self.body = body
