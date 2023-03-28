from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class VerifyEmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.verified) 

class UnsubscribeTokenGenerator():
    def _make_hash_value(self, user):
        return six.text_type(user.id) + six.text_type(user.email) + six.text_type(user.active)
    

email_verification_token = VerifyEmailTokenGenerator()
unsubscribe_token = UnsubscribeTokenGenerator()

