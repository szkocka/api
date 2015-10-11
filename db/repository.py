from db.model import User, News, Forum, Research, db


def save(obj):
    db.session.add(obj)
    db.session.commit()


def update():
    db.session.commit()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user(email, hashed_pass):
    return User.query.filter_by(email=email, hashed_password=hashed_pass).first()


def all_news():
    return News.query.all().order_by(News.created.desc())


def all_researches():
    return Research.query.all()


def get_user(_id):
    return User.query.get(_id)


def get_research(_id):
    return Research.query.get(_id)


def get_forum(_id):
    return Forum.query.get(_id)
