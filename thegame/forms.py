from django import forms
from .models import Question, Answer

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


