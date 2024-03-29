from django.db import models
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django import forms

from codingroutine.tokens import email_verification_token, unsubscribe_token
from administration.models import ExceptionTracker

import traceback


EASY="EASY"
MED="MEDIUM"
HARD="HARD"
DIFFICULTY_CHOICES=((EASY, "Easy"), (MED, "Medium"), (HARD, "Hard"))
class Newsletter_User(models.Model):

    email = models.CharField(max_length=200)
    exercises_received = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    unsubscribe_token = models.CharField(max_length=200, default="")

    class Meta: ordering = ['-created']
    def __str__(self): return self.email

    @classmethod
    def get_users(cls): return cls.objects.filter()

    @classmethod
    def get_verified_users(cls): return cls.objects.filter(verified=True)

    def generate_verification_email(self, request):
        '''
        Render email template
        Attach alternatives: text_content and html template
        '''
        try:
         mail_subject = "Verify your email address"
         message = render_to_string('base/email_templates/template_verification_email.html',
         {'domain': get_current_site(request).domain,
        'uid':  urlsafe_base64_encode(force_bytes(self.id)),
        'token': email_verification_token.make_token(self),
        'protocol': 'https' if request.is_secure() else 'http',
        'unsubscribe_token': self.unsubscribe_token}) 
         text_conent = strip_tags(message)
         email = EmailMultiAlternatives(mail_subject, text_conent, to=[self.email])
         email.attach_alternative(message, "text/html")

         return email
        except Exception:
         ExceptionTracker.objects.create(
         title='Failed to generate verification email', exception=traceback.format_exc())

    def generate_daily_coding_exercise(self):

        '''
        Get coding exercise based on already received amount
        '''
        try:
         coding_exercise = CodingExercise.objects.get(id= self.exercises_received + 1)
         return coding_exercise
        except Exception:
         ExceptionTracker.objects.create(
         title='Failed to generate daily coding exercise', exception=traceback.format_exc())

    def generate_welcoming_email(self, request):
        '''
        Render email template
        Attach alternatives: text_content and html template
        '''
        try:
         mail_subject = "Welcome on board!"
         message = render_to_string(
         'base/email_templates/template_welcome_email.html', {"unsubscribe_token": self.unsubscribe_token, 
         'uid':  urlsafe_base64_encode(force_bytes(self.id)), 'protocol': 'https' if request.is_secure() else 'http', 'domain': get_current_site(request).domain,})
         text_conent = strip_tags(message)
         email = EmailMultiAlternatives(mail_subject, text_conent, to=[self.email])
         email.attach_alternative(message, "text/html")
         return email

        except Exception:
         ExceptionTracker.objects.create(
         title='Failed to generate welcoming email', exception=traceback.format_exc())


class MessageContact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_contact = models.CharField(max_length=200)
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000)
    unread = models.BooleanField(default=True)

    class Meta:ordering = ['-sent']
    def __str__(self): return self.message

    @classmethod
    def get_messages(cls): return cls.objects.filter()

    @classmethod
    def get_unread_messages(cls): return cls.objects.filter(unread=True)
    
    def make_read(self):
        if self.unread:
         self.unread = False 
         self.save()  


class CodingExercise(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default="Easy")
    example_input = models.CharField(max_length=200, null=True, blank=True)
    example_output = models.CharField(max_length=200, null=True, blank=True)
    body = models.CharField(max_length=1000)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.title if self.title else self.body
    class Meta:ordering = ['-added']
    
    @classmethod
    def get_exercises(cls): return cls.objects.filter()


    def update_exercise(self, request):
        '''
        Update already existing exercise
        '''
        try:

            # make sure difficulty is set
            difficulty = request.POST.get('difficulty').capitalize()
            self.difficulty = self.difficulty if difficulty == "" else difficulty 
            self.title = request.POST.get('title').capitalize()
            self.body = request.POST.get('body')
            self.example_input = request.POST.get('example_input')
            self.example_output = request.POST.get('example_output')
            self.save()
        except Exception: 
            ExceptionTracker.objects.create(
            title=f'Failed to update exercise {self.title}', exception=traceback.format_exc())

        return self

