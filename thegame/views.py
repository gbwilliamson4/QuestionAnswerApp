from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login


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

    # if request.method != 'POST':
    #     # No data submitted; create a blank form.
    #     form = AnswerForm()
    # else:
    #     # POST data submitted; process data.
    #     form = AnswerForm(data=request.POST)
    #     if form.is_valid():
    #         print(form)
    #         form.save()
    #         return redirect('george_answers')

    context = {'questions': questions}
    # context = {'questions': questions}
    return render(request, 'thegame/kelsy_answers.html', context)


def george_answers(request):
    questions = Question.objects.all()

    for question in questions:
        ans = question.answer_set.first()
        if ans is not None:
            print(ans)

    context = {'questions': questions}
    # context = {'questions': questions}
    return render(request, 'thegame/george_answers.html', context)


def comparing(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'thegame/comparing.html', context)

def save_answer(request, question_pk, person):
    # print(question_pk)
    print("request.post", request.POST)
    # print(request.POST['person'])
    print(person)
    question = Question.objects.get(pk=question_pk)
    person = People.objects.get(person=person)

    ans = request.POST['answer']
    a = Answer(question=question, answer=ans, person=person)
    a.save()

    return redirect('george_answers')


# def save_k_answer(request, question_pk):
#     question = Question.objects.get(pk=question_pk)
#
#     ans = request.POST['answer']
#     a = KelsyAnswer(question=question, answer=ans)
#     a.save()
#
#     return redirect('kelsy_answers')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'thegame/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            redirect('index')
    else:
        return render(request, 'thegame/login.html', {})