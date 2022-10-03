from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)
        labels = {'question': 'Question'}

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ('answer',)
#         labels = {'answer': ':'}

class GeorgeAnswerForm(forms.ModelForm):
    class Meta:
        model = GeorgeAnswer
        fields = ('answer',)
        labels = {'answer': ':'}

class KelsyAnswerForm(forms.ModelForm):
    class Meta:
        model = KelsyAnswer
        fields = ('answer',)
        labels = {'answer': ':'}

