class InviteToJoin(object):
    def __init__(self, supervisor, title, description, researcher, text):
        self.supervisor = supervisor
        self.title = title
        self.description = description
        self.researcher = researcher
        self.text = text

    def supervisor(self):
        return self.supervisor

    def title(self):
        return self.title

    def description(self):
        return self.description

    def researcher(self):
        return self.researcher

    def text(self):
        return self.text


class InviteToJoinSubj(object):
    def __init__(self, supervisor, title):
        self.supervisor = supervisor
        self.title = title

    def supervisor(self):
        return self.supervisor

    def title(self):
        return self.title


class ReqToJoinSubj(object):
    def __init__(self, user, title):
        self.user = user
        self.title = title

    def user(self):
        return self.user

    def title(self):
        return self.title


class ReqToJoin(object):
    def __init__(self, user, title, supervisor, text):
        self.user = user
        self.title = title
        self.supervisor = supervisor
        self.text = text

    def supervisor(self):
        return self.supervisor

    def user(self):
        return self.user

    def title(self):
        return self.title

    def text(self):
        return self.text


class NewMessage(object):
    def __init__(self, researcher, message_creator, forum, text, research_id, forum_id):
        self.researcher = researcher
        self.message_creator = message_creator
        self.forum = forum
        self.text = text
        self.research_id = research_id
        self.forum_id = forum_id

    def researcher(self):
        return self.researcher

    def message_creator(self):
        return self.message_creator

    def forum(self):
        return self.forum

    def text(self):
        return self.text

    def research_id(self):
        return self.research_id

    def forum_id(self):
        return self.forum_id


class NewMessageSubj(object):
    def __init__(self, forum, research):
        self.forum = forum
        self.research = research

    def forum(self):
        return self.forum

    def research(self):
        return self.research


class ResetPasswordSubj(object):
    def __init__(self, user):
        self.user = user

    def user(self):
        return self.user


class ResetPasswordBody(object):
    def __init__(self, user, url):
        self.user = user
        self.url = url

    def user(self):
        return self.user

    def url(self):
        return self.url
