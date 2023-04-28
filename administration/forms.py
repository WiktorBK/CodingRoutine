from django.forms import ModelForm
from django import forms
from base.models import CodingExercise
from django.contrib.auth.models import User


class AddExerciseForm(ModelForm):
    class Meta:
        model=CodingExercise
        fields = '__all__'
        widgets ={
            'difficulty': forms.TextInput(attrs={'id': 'difficulty-form', 'maxlength':'1000'}),
            'title': forms.TextInput(attrs={'id':'title-form', 'type': 'text', 'placeholder': 'Exercise title',}),
            'body': forms.Textarea(attrs={'id':'body-form', 'type': 'text', 'placeholder': 'Exercise body',}),
            'example_input': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [2, 3, 4, 5]'}),
            'example_output': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [5, 4, 3, 2]'})
        }

class EditExerciseForm(ModelForm):

    def __init__(self, exercise, *args, **kwargs):
        super(EditExerciseForm, self).__init__(*args, **kwargs)
        try:
            # add dynamic values

            self.fields['title'].widget.attrs["value"] = exercise.title
            self.fields['body'].widget.attrs["value"] = exercise.body
            self.fields['example_input'].widget.attrs["value"] = exercise.example_input
            self.fields['example_output'].widget.attrs["value"] = exercise.example_output
        except: pass

    class Meta:
        model=CodingExercise
        fields = '__all__'
        widgets ={
            'difficulty': forms.TextInput(attrs={'id': 'difficulty-form', 'maxlength':'1000'}),
            'title': forms.TextInput(attrs={'id':'title-form', 'type': 'text', 'placeholder': 'Exercise title'}),
            'body': forms.Textarea(attrs={'id':'body-form', 'type': 'text', 'placeholder': 'Exercise body'}),
            'example_input': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [2, 3, 4, 5]'}),
            'example_output': forms.TextInput(attrs={'id':'example-form', 'type': 'text', 'placeholder': 'e.g [5, 4, 3, 2]'})
        }








        