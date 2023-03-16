from django.forms import ModelForm
from django import forms
from .models import Newsletter_User, Message_contact

class NewsletterUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Enter your email', 'id': 'email', 'type':"text"}))



class MessageContactForm(ModelForm):
    class Meta:
        model = Message_contact
        fields = '__all__'