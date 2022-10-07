from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from random import randint  # Used for generating random 3 digit room numbers.


def index(request):
    context = {}
    return render(request, 'thegame/index.html', context)


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
            return redirect('index')
    else:
        return render(request, 'thegame/login.html', {})


@login_required
def new_question(request):
    """Add a new question."""
    # Get room num and questions in that room.
    room_num = request.user.room_set.first()
    room_num_id = room_num.pk
    questions = Question.objects.filter(room=room_num_id)
    context = {'questions': questions}
    return render(request, 'thegame/new-question.html', context)


@login_required
def save_question(request):
    room_num = request.user.room_set.first()
    question_txt = request.POST['question']
    question = Question(room=room_num, question=question_txt)
    question.save()
    return redirect('new-question')


@login_required
def answers(request):
    room_num = request.user.room_set.first()
    questions = Question.objects.filter(room=room_num)

    # Lets loop through the questions, get the answers, pile them into a new dict
    info = {}
    for question in questions:
        answer = Answer.objects.filter(user=request.user).filter(question__in=Question.objects.filter(pk=question.pk))
        info[question] = answer

    context = {'answers': answers, 'questions': questions, 'info': info}
    return render(request, 'thegame/answers.html', context)


@login_required
def save_answer(request, question_pk):
    print("request.post", request.POST)
    question = Question.objects.get(pk=question_pk)
    person = request.user
    print(person)

    ans = request.POST['answer']
    a = Answer(question=question, answer=ans, user=person)
    a.save()

    return redirect('answers')


@login_required
def comparing(request):
    room_num = request.user.room_set.first()
    questions = Question.objects.filter(room=room_num)

    # Lets loop through the questions, get the answers, pile them into a new list or something
    info = {}
    for question in questions:
        # print('question pk', question.pk)
        answer = Answer.objects.filter(question__in=Question.objects.filter(pk=question.pk))
        info[question] = answer

    context = {'info': info}
    return render(request, 'thegame/comparing.html', context)
    # return render(request, 'thegame/comparing.html', context)


@login_required
def rooms(request):
    rooms = Room.objects.filter(user=request.user)
    room_hist = Room_History.objects.filter(user=request.user)
    context = {'rooms': rooms, 'room_hist': room_hist}
    return render(request, 'thegame/rooms.html', context)


@login_required
def new_room(request):
    # Get a 3 digit room number, create database instance, link room to user via foreign key in Room model.
    room_num = randint(100, 999)
    room = Room(room_number=room_num)
    room.save()
    room.user.add(request.user)
    room.save()
    log_room_history(room, request.user)
    return redirect('rooms')


@login_required
def leave_room(request):
    # get the current room the user is in, remove user from Room model, save.
    room = Room.objects.filter(user=request.user)
    room = room[0]
    room.user.remove(request.user)
    room.save()
    return redirect('rooms')


@login_required
def join_room(request):
    # get the desired room number from the form, get current user, add user to Room model via foreign key.
    num = request.POST['room-num']
    num = int(num)  # make sure that its an integer.
    user = request.user
    room = Room.objects.filter(room_number=num)
    room = room[0]
    room.user.add(user)
    room.save()
    log_room_history(room, user)
    return redirect('rooms')


def log_room_history(room, user):
    # Create instance of model, pass in the user and room num, save.
    try:
        room_history = Room_History(room=room, user=user)
        room_history.save()
    except:
        # No action required. History for this room/user combo already exists.
        pass


def delete_unused_rooms():
    # remove rooms that are either empty or have no questions associated with them.
    unused_rooms = Question.room.filter(pk>1)
    print('unused rooms:', unused_rooms)


import os
@login_required
def testing(request):
    # delete_unused_rooms()
    print('os.getcwd():', os.getcwd())
    room_num = request.user.room_set.first()
    questions = Question.objects.filter(room=room_num)

    # Lets loop through the questions, get the answers, pile them into a new list or something
    info = {}
    for question in questions:
        # print('question pk', question.pk)
        answer = Answer.objects.filter(question__in=Question.objects.filter(pk=question.pk))
        info[question] = answer

    context = {'info': info}
    return render(request, 'thegame/tests.html', context)
