from django.forms import ModelForm
from .models import Newsletter_User, Message_contact

class NewsletterUserForm(ModelForm):
    class Meta:
        model = Newsletter_User
        fields = ['email']


class MessageContactForm(ModelForm):
    class Meta:
        model = Message_contact
        fields = '__all__'