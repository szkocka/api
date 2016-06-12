from flask import request

from flask.ext.restful import Resource

from emails.sender import send_email
from emails.views import NewMessageSubj, NewMessage
from model.db import Research, Message

from common.http_responses import ok_msg
from model.docs import ResearchIndex


class IndexResearch(Resource):
    def post(self):
        research_id = int(request.json['research_id'])
        research = Research.get(research_id)

        ResearchIndex(research).put()

        return ok_msg('Research indexed.')


class NotifyAboutNewMessage(Resource):
    def post(self):
        message_id = int(request.json['message_id'])
        message = Message.get(message_id)

        message_creator_key = message.creator_key
        message_creator = message_creator_key.get()
        forum = message.forum_key.get()
        research = forum.research_key.get()

        for researcher_key in research.researchers_keys:
            if researcher_key != message_creator_key:
                researcher = researcher_key.get()

                subj = NewMessageSubj(forum.subject, research.title)
                body = NewMessage(researcher.name, message_creator.name,
                                  forum.subject, message.text,
                                  research.key.id(), forum.key.id())

                send_email(subj, body, researcher.email)

        return ok_msg('Notification sent.')
