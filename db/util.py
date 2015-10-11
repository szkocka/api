from db.model import User, News, Forum, Research


class DB:
    def __init__(self, sql):
        self.sql = sql

    def save(self, obj):
        self.sql.session.add(obj)
        self.sql.session.commit()

    def update(self):
        return self.sql.session.commit()

    def find_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def find_user(self, email, hashed_pass):
        return User.query.filter_by(email=email, hashed_password=hashed_pass).first()

    def all_news(self):
        return News.query.all().order_by(News.created.desc())

    def all_researches(self):
        return Research.query.all()

    def get_user(self, _id):
        return User.query.get(_id)

    def get_research(self, _id):
        return Research.query.get(_id)

    def get_forum(self, _id):
        return Forum.query.get(_id)
