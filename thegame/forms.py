from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)
        labels = {'question': 'Question'}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer',)
        labels = {'answer': ':'}

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

