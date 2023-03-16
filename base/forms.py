from django.forms import ModelForm
from .models import Newsletter_User

class NewsletterUserForm(ModelForm):
    class Meta:
        model = Newsletter_User
        fields = ['email']