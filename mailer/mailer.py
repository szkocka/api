import boto.ses
import pystache
import boto.pyami.config

class Mailer:
    def __init__(self):
        self.renderer = pystache.Renderer()
        self.from_email = 'kavf.mukola@gmail.com'
        self.connection = boto.ses.connect_to_region('eu-west-1')

    def send(self, subj_view, body_view, recipients):
        subj = self.renderer.render(subj_view)
        body = self.renderer.render(body_view)

        self.connection.send_email(self.from_email, subj, body, recipients)
