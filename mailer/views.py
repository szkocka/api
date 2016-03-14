class InviteToJoin(object):
    def __init__(self, json):
        self.supervisor = json['supervisor']
        self.title = json['title']
        self.description = json['description']
        self.researcher = json['researcher']
        self.text = json['text']

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
    def __init__(self, json):
        self.supervisor = json['supervisor']
        self.title = json['title']

    def supervisor(self):
        return self.supervisor

    def title(self):
        return self.title


class ReqToJoinSubj(object):
    def __init__(self, json):
        self.user = json['user']
        self.title = json['title']

    def user(self):
        return self.user

    def title(self):
        return self.title


class ReqToJoin(object):
    def __init__(self, json):
        self.user = json['user']
        self.title = json['title']
        self.supervisor = json['supervisor']
        self.text = json['text']

    def supervisor(self):
        return self.supervisor

    def user(self):
        return self.user

    def title(self):
        return self.title

    def text(self):
        return self.text
