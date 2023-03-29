from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import time
import base64

class VerifyEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.verified) 

class UnsubscribeTokenGenerator():
    def generate_unsubscribe_token(self, user):
        return base64.b64encode(str(user.id).encode("ascii") + user.email.encode("ascii") + str(time.time()).encode("ascii")
                                 + str(user.verified).encode("ascii")).decode('ascii')
    

email_verification_token = VerifyEmailTokenGenerator()
unsubscribe_token = UnsubscribeTokenGenerator()

