from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes

from .tokens import email_verification_token, unsubscribe_token

class Newsletter_User(models.Model):

    email = models.CharField(max_length=200)
    excercises_received = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    unsubscribe_token = models.CharField(max_length=200, default="")

    class Meta: ordering = ['-created']
    def __str__(self): return self.email

    @classmethod
    def get_users(cls): return cls.objects.filter()


    def generate_verification_email(self, request):
        try:
         mail_subject = "Verify your email address"
         message = render_to_string('base/email_templates/template_verification_email.html',
         {
        'domain': get_current_site(request).domain,
        'uid':  urlsafe_base64_encode(force_bytes(self.id)),
        'token': email_verification_token.make_token(self),
        'protocol': 'https' if request.is_secure() else 'http',
        'unsubscribe_token': self.unsubscribe_token
         })
         email = EmailMessage(mail_subject, message, to=[self.email])
         return email
        except Exception as e:
         ExceptionTracker.objects.create(
         title='Failed to generate verification email', exception=e)

    def generate_daily_coding_excercise(self):
        try:
         coding_excercise = CodingExcercise.objects.get(id= self.excercises_received + 1)
         return coding_excercise
        except Exception as e:
         ExceptionTracker.objects.create(
         title='Failed to generate daily coding excercise', exception=e)

    def generate_welcoming_email(self):
        try:
         mail_subject = "Welcome on board!"
         message = render_to_string(
         'base/email_templates/template_welcome_email.html', {"unsubscribe_token": self.unsubscribe_token})
         email = EmailMessage(mail_subject, message, to=[self.email])
         return email

        except Exception as e:
         ExceptionTracker.objects.create(
         title='Failed to generate welcoming email', exception=e)



class Message_contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_contact = models.CharField(max_length=200)
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    unread = models.BooleanField(default=True)


    class Meta:ordering = ['-sent']
    def __str__(self): return self.message

    @classmethod
    def get_messages(cls): return cls.objects.filter()

    @classmethod
    def get_unread_messages(cls): return cls.objects.filter(unread=True)



class CodingExcercise(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=15)
    example_input = models.CharField(max_length=200, null=True, blank=True)
    example_output = models.CharField(max_length=200, null=True, blank=True)
    body = models.CharField(max_length=500)

    def __str__(self): return self.title if self.title else self.body

    @classmethod
    def get_excercises(cls): return cls.objects.filter()


class ExceptionTracker(models.Model):
    occured = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    exception = models.CharField(max_length=300)
    unread = models.BooleanField(default=True)

    class Meta:ordering = ['-occured']
    def __str__(self): return self.title

    @classmethod
    def get_exceptions(cls): return cls.objects.filter()

    @classmethod
    def get_unread_exceptions(cls): return cls.objects.filter(unread=True)
