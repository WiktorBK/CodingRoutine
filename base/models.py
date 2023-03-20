from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from .tokens import email_verification_token

class Newsletter_User(models.Model):

    email = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def generate_verification_email(self, request, user, to_email):
        mail_subject = "Verify your email address"
        message = render_to_string('base/template_email.html', 
            {
            'domain': get_current_site(request).domain,
            'uid':  urlsafe_base64_encode(force_bytes(user.id)),
            'token': email_verification_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
            })
        email = EmailMessage(mail_subject, message, to = [to_email])

        return email
            
        


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
