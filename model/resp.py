import logging

from model.db import RelationshipType


class BaseJsonResponce:
    def js(self):
        logging.info(self.__dict__)
        return self.__dict__


class UserJson(BaseJsonResponce):
    def __init__(self, user):
        self.id = user.key.id()
        self.name = user.name
        self.email = user.email
        self.status = user.status
        self.supervisor_in = user.supervisor_in
        self.researcher_in = user.researcher_in
        self.created_forums = user.created_forums
        self.posted_messages = user.posted_messages


class UserDetailsJson(UserJson):
    def __init__(self, user, supervisor_of, researcher_in):
        UserJson.__init__(self, user)
        self.cv = user.cv
        self.supervisor_of = map(lambda r: ResearchJson(r, {}).js(), supervisor_of)
        self.researcher_in = map(lambda r: ResearchJson(r, {}).js(), researcher_in)


class ResearchJson(BaseJsonResponce):
    def __init__(self, research, relationship_types):
        self.id = research.key.id()
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
        self.relationship_type = relationship_types.get(self.id, RelationshipType.NONE)


class ResearchDetailsJson(ResearchJson):
    def __init__(self, research, relationship_types):
        ResearchJson.__init__(self, research, relationship_types)
        self.supervisor = UserJson(research.supervisor_key.get()).js()
        self.researchers = map(lambda key: UserJson(key.get()).js(),
                               research.researchers_keys)


class ForumJson(BaseJsonResponce):
    def __init__(self, forum):
        self.id = forum.key.id()
        self.createdBy = UserJson(forum.creator_key.get()).js()
        self.created = forum.creation_time.strftime('%Y-%m-%d %H:%M:%S')
        self.subject = forum.subject
        self.research = forum.research_key.id()
        self.status = forum.status


class NewsJson(BaseJsonResponce):
    def __init__(self, n):
        self._id = n.key.id()
        self.createdBy = UserJson(n.creator_key.get()).js()
        self.created = n.creation_time.strftime('%Y-%m-%d %H:%M:%S')
        self.title = n.title
        logging.info(n.title)
        logging.info(self.title)
        self.body = n.body
        self.image_url = n.image_url


class MessageJson(BaseJsonResponce):
    def __init__(self, message):
        self.id = message.key.id(),
        self.createdBy = UserJson(message.creator_key.get()).js(),
        self.created = message.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        self.message = message.text


class MyInvitationJson(BaseJsonResponce):
    def __init__(self, invitation):
        self.id = invitation.key.id()
        research = invitation.research_key.get()
        self.research_name = research.title


class ResearchIdJson(BaseJsonResponce):
    def __init__(self, research_key):
        self.research_id = research_key.id()


class NewsIdJson(BaseJsonResponce):
    def __init__(self, news_key):
        self.news_id = news_key.id()


class ForumIdJson(BaseJsonResponce):
    def __init__(self, forum_key):
        self.forum_id = forum_key.id()


class MessageIdJson(BaseJsonResponce):
    def __init__(self, message_key):
        self.message_id = message_key.id()


class TagsJson(BaseJsonResponce):
    def __init__(self, tags):
        self.tags = tags


class ListNewsJson(BaseJsonResponce):
    def __init__(self, news, cursor):
        self.news = map(lambda n: NewsJson(n).js(), news)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ListResearchesJson(BaseJsonResponce):
    def __init__(self, researches, relationship_types, cursor):
        self.researches = map(lambda r: ResearchDetailsJson(r, relationship_types).js(), researches)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ListForumsJson(BaseJsonResponce):
    def __init__(self, forums, cursor):
        self.forums = map(lambda f: ForumJson(f).js(), forums)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ListMessagesJson(BaseJsonResponce):
    def __init__(self, messages, cursor):
        self.messages = map(lambda m: MessageJson(m).js(), messages)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ListMyInvitations(BaseJsonResponce):
    def __init__(self, researches):
        self.researches = map(lambda r: ResearchJson(r, {}).js(), researches)


class ListReqToJoin(BaseJsonResponce):
    def __init__(self, users):
        self.users = map(lambda u: UserJson(u).js(), users)


class ListUsers(BaseJsonResponce):
    def __init__(self, users, cursor):
        self.users = map(lambda u: UserJson(u).js(), users)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ListUserResearchesJson(BaseJsonResponce):
    def __init__(self, researches, relationship_types, cursor):
        self.researches = map(lambda r: ResearchJson(r, relationship_types).js(), researches)

        self.cursor = None
        if cursor:
            self.cursor = cursor.urlsafe()


class ResearchesSearchResultJson(BaseJsonResponce):
    def __init__(self, researches):
        self.researches = map(lambda r: ResearchDetailsJson(r, {}).js(), researches)


