import logging
from google.appengine.api import mail
import pystache
from init import config


class Mailer:
    def __init__(self):
        self.renderer = pystache.Renderer()

    def send(self, subj_view, body_view, recipient):
        subj = self.renderer.render(subj_view)
        body = self.renderer.render(body_view)

        logging.info('Sending email')
        mail.send_mail(sender=config.FROM_EMAIL, to=recipient,
                       subject=subj, body=body)
