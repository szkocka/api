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
