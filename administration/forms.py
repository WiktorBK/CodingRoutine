from django.forms import ModelForm
from django import forms
from base.models import CodingExcercise
from django.contrib.auth.models import User


class AddExcerciseForm(ModelForm):
    class Meta:
        model=CodingExcercise
        fields = '__all__'
        widgets ={
            'difficulty': forms.TextInput(attrs={'id': 'difficulty-form', 'maxlength':'1000'}),
            'title': forms.TextInput(attrs={'id':'title-form', 'type': 'text', 'placeholder': 'Excercise title',}),
            'body': forms.Textarea(attrs={'id':'body-form', 'type': 'text', 'placeholder': 'Excercise body',}),
            'example_input': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [2, 3, 4, 5]'}),
            'example_output': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [5, 4, 3, 2]'})
        }






        