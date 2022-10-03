from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, People
from django.urls import reverse

# def index(request):
#     return HttpResponse("Welcome to the index page.")

def index(request):
    context = {}
    return render(request, 'thegame/index.html', context)


def new_question(request):
    """Add a new topic."""
    questions = Question.objects.all()
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = QuestionForm()
    else:
        # POST data submitted; process data.
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_question')

    # Display a blank or invalid form.
    context = {'form': form, 'questions': questions}
    return render(request, 'thegame/new_question.html', context)


def kelsy_answers(request):
    answers = Answer.objects.all()
    context = {'answers': answers}
    return render(request, 'thegame/kelsy_answers.html', context)


def george_answers(request):
    questions = Question.objects.all()

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = AnswerForm()
    else:
        # POST data submitted; process data.
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('george_answers')

    context = {'questions': questions, 'form': form}
    # context = {'questions': questions}
    return render(request, 'thegame/george_answers.html', context)


def comparing(request):
    context = {}
    return render(request, 'thegame/comparing.html', context)

def save_g_answer(request, question_pk):
    # print(question_pk)
    # print("request.post", request.POST)
    # print(request.POST['answer'])
    person = People.objects.get(person='George')
    question = Question.objects.get(pk=question_pk)

    ans = request.POST['answer']
    a = Answer(person=person, question=question, answer=ans)
    a.save()

    return redirect('george_answers')
    # return redirect('thegame/george_answers.html')