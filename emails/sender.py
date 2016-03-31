import logging
import os

from google.appengine.api import mail
import pystache


def send_email(subj_view, body_view, recipient):
    renderer = pystache.Renderer()
    sender = os.environ['SENDER_EMAIL']

    subj = renderer.render(subj_view)
    body = renderer.render(body_view)

    logging.info('Sending email')
    mail.send_mail(sender=sender, to=recipient,
                   subject=subj, body=body)
