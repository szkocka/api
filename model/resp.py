class BaseJsonResponce:
    def to_json(self):
        return self.__dict__


class UserJson(BaseJsonResponce):
    def __init__(self, user):
        self.id = user.key.id()
        self.name = user.name
        self.email = user.email


class UserDetailsJson(UserJson):
    def __init__(self, user, supervisor_of, researcher_in):
        UserJson.__init__(self, user)
        self.cv = user.cv
        self.supervisor_of = map(lambda r: ResearchJson(r).to_json(), supervisor_of)
        self.researcher_in = map(lambda r: ResearchJson(r).to_json(), researcher_in)


class ResearchJson(BaseJsonResponce):
    def __init__(self, research):
        self._id = research.key.id()
        self.created = research.creation_time.strftime('%Y-%m-%d %H:%M:%S')
        self.title = research.title
        self.tags = research.tags
        self.area = research.area
        self.status = research.status
        self.description = {
                       'brief': research.brief_desc,
                       'detailed': research.detailed_desc
                   }
        self.image_url = research.image_url


class NewsJson(BaseJsonResponce):
    def __init__(self, n):
        self._id = n.key.id()
        self.createdBy = UserJson(n.creator_key.get()).to_json(),
        self.created = n.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        self.title = n.title,
        self.body = n.body
        self.image_url = n.image_url


class NewsListJson(BaseJsonResponce):
    def __init__(self, news):
        self.news = map(lambda n: NewsJson(n).to_json(), news)


class ResearchIdJson(BaseJsonResponce):
    def __init__(self, research_key):
        self.research_id = research_key.id()


class TagsJson(BaseJsonResponce):
    def __init__(self, tags):
        self.tags = tags
