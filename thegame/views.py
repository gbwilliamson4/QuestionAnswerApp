from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
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
    questions = Question.objects.all()

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = KelsyAnswerForm()
    else:
        # POST data submitted; process data.
        form = KelsyAnswerForm(data=request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('george_answers')

    context = {'questions': questions, 'form': form}
    # context = {'questions': questions}
    return render(request, 'thegame/kelsy_answers.html', context)


def george_answers(request):
    questions = Question.objects.all()

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = GeorgeAnswerForm()
    else:
        # POST data submitted; process data.
        form = GeorgeAnswerForm(data=request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('george_answers')

    context = {'questions': questions, 'form': form}
    # context = {'questions': questions}
    return render(request, 'thegame/george_answers.html', context)


def comparing(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'thegame/comparing.html', context)

def save_g_answer(request, question_pk):
    # print(question_pk)
    # print("request.post", request.POST)
    # print(request.POST['answer'])
    question = Question.objects.get(pk=question_pk)

    ans = request.POST['answer']
    a = GeorgeAnswer(question=question, answer=ans)
    a.save()

    return redirect('george_answers')


def save_k_answer(request, question_pk):
    question = Question.objects.get(pk=question_pk)

    ans = request.POST['answer']
    a = KelsyAnswer(question=question, answer=ans)
    a.save()

    return redirect('kelsy_answers')