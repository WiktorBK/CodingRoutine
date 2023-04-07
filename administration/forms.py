from django.forms import ModelForm
from django import forms
from base.models import CodingExcercise


class AddExcerciseForm(ModelForm):
    class Meta:
        model=CodingExcercise
        fields = '__all__'
        widgets ={
            'title': forms.TextInput(attrs={'id':'excercise-form', 'type': 'text', 'placeholder': 'Excercise title',}),
            'body': forms.Textarea(attrs={'id':'excercise-form', 'type': 'text', 'placeholder': 'Excercise body',}),
            'example_input': forms.TextInput(attrs={'id':'excercise-form', 'type': 'text', 'placeholder': 'e.g [2, 3, 4, 5]'}),
            'example_output': forms.TextInput(attrs={'id':'excercise-form', 'type': 'text', 'placeholder': 'e.g [5, 4, 3, 2]'})

        }





        