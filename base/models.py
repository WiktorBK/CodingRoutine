from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings

class Newsletter_User(models.Model):
    email = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def send_email(self, to_email, first_name):
        email = EmailMessage(
            f"Verify your email",
            f"Hello, {first_name}! Thank you for subscribing to codingRoutine!",
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
        )
        email.send()

    class Meta: ordering = ['-created']
    def __str__(self): return self.email
    


class Message_contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_contact = models.CharField(max_length=200)
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


    class Meta: ordering = ['-sent']
    def __str__(self): return self.message
