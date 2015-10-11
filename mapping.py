from resources.auth import AuthLocalLogin
from resources.forums import ListForums, AddForum, GetForum, AddMessage
from resources.me import Me
from resources.news import AddNews, ListNews
from resources.emails import InviteToJoinResearch, ReqToJoinResearch
from resources.researches import AddResearch, ListResearches, GetResearch, UpdateResearch
from resources.upload import Upload
from resources.users import CreateUser


def resource_mapping(api):
    api.add_resource(AddNews, '/news')
    api.add_resource(ListNews, '/news')
    api.add_resource(AddResearch, '/researches')
    api.add_resource(ListResearches, '/researches')
    api.add_resource(GetResearch, '/researches/<research_id>')
    api.add_resource(UpdateResearch, '/researches/<research_id>')
    api.add_resource(GetForum, '/researches/forums/<forum_id>')
    api.add_resource(AddMessage, '/researches/forums/<forum_id>')
    api.add_resource(ListForums, '/researches/<research_id>/forums')
    api.add_resource(AddForum, '/researches/<research_id>/forums')
    api.add_resource(InviteToJoinResearch, '/researches/<research_id>/invite')
    api.add_resource(ReqToJoinResearch, '/researches/<research_id>/join')
    api.add_resource(CreateUser, '/users')
    api.add_resource(AuthLocalLogin, '/auth/local')
    api.add_resource(Me, '/users/me')
    api.add_resource(Upload, '/upload')
