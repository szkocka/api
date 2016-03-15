import logging

from google.appengine.api import mail

import pystache
from main import app

renderer = pystache.Renderer()


def send_email(subj_view, body_view, recipient):
    subj = __render_view(subj_view)
    body = __render_view(body_view)

    logging.info('Sending email')
    mail.send_mail(sender=app.config['FROM_EMAIL'],
                   to=recipient, subject=subj, body=body)


def __render_view(view):
    return renderer.render(view)
