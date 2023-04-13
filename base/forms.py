from django.forms import ModelForm
from django import forms
from .models import Newsletter_User, MessageContact

class NewsletterUserForm(ModelForm):

    class Meta:
        model = Newsletter_User
        fields = ['email']
        widgets ={
            'email': forms.TextInput(attrs={'id':'email', 'type': 'text', 'placeholder': 'Enter email adress', 'autocomplete': "off"})
        }


class MessageContactForm(ModelForm):   
    class Meta:
        model = MessageContact
        fields = '__all__'
        widgets ={
            'email_contact': forms.TextInput(attrs={'id':'email-contact', 'type': 'text', 'placeholder': 'Email adress', "name": "email", "style": "border-radius:10px"}),
            'first_name': forms.TextInput(attrs={'id':'inline', 'type': 'text', 'placeholder': 'First name', "style": "border-radius:10px"}),
            'last_name': forms.TextInput(attrs={'id':'inline', 'type': 'text', 'placeholder': 'Last name', "style": "border-radius:10px"}),
            'message': forms.Textarea(attrs={'id':'message', 'type': 'text', 'placeholder': 'Write something...'})
        }

        


        