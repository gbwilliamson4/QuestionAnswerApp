from django.http import HttpResponse
from django.shortcuts import render, redirect
from psycopg2 import IntegrityError
from sqlite3 import IntegrityError

from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint  # Used for generating random 3 digit room numbers.
from django.contrib import messages


def index(request):
    context = {}
    return render(request, 'thegame/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('index')

    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'thegame/signup.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, "Login Successful.")
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/password combination.')
            return redirect('login')
    else:
        # messages.error(request, 'Problem! Sooo many problems!')
        # return redirect('login')
        return render(request, 'thegame/login.html', {})


def logout_user(request):
    logout(request)
    # messages.success(request, 'You have been successfully logged out. Please come again soon.')
    return render(request, 'thegame/logout.html')

@login_required
def new_question(request):
    """Add a new question."""
    # Get room num and questions in that room.
    room_num = request.user.room_set.first()
    if room_num is None:
        return redirect('rooms')
    else:
        questions = Question.objects.filter(room=room_num)
        context = {'questions': questions}
    return render(request, 'thegame/new-question.html', context)


@login_required
def save_question(request):
    room_num = request.user.room_set.first()
    if room_num is None:
        return redirect('rooms')
    # Send Message saying you need to join a room first or something.
    else:
        question_txt = request.POST['question']
        question = Question(room=room_num, question=question_txt)
        question.save()
    return redirect('new-question')


@login_required
def answers(request):
    room_num = request.user.room_set.first()
    questions = Question.objects.filter(room=room_num)

    if room_num is None:
        return redirect('rooms')
    else:
        # Lets loop through the questions, get the answers, pile them into a new dict
        info = {}
        for question in questions:
            answer = Answer.objects.filter(user=request.user).filter(question__in=Question.objects.filter(pk=question.pk))
            info[question] = answer

        context = {'answers': answers, 'questions': questions, 'info': info}
    return render(request, 'thegame/answers.html', context)


@login_required
def save_answer(request, question_pk):
    # Get the question, get the user's text, save as an Answer.
    question = Question.objects.get(pk=question_pk)
    person = request.user

    ans = request.POST['answer']
    a = Answer(question=question, answer=ans, user=person)
    a.save()

    return redirect('answers')


@login_required
def comparing(request):
    room_num = request.user.room_set.first()
    questions = Question.objects.filter(room=room_num)

    if room_num is None:
        return redirect('rooms')
    else:
        # Lets loop through the questions, get the answers, pile them into a new dict
        info = {}
        for question in questions:
            answer = Answer.objects.filter(question__in=Question.objects.filter(pk=question.pk))
            info[question] = answer

        context = {'info': info}
    return render(request, 'thegame/comparing.html', context)


@login_required
def rooms(request):
    rooms = Room.objects.filter(user=request.user)
    room_hist = Room_History.objects.filter(user=request.user)

    # if user is already in a room, find out who else is in that room.
    if rooms:
        room = rooms[0]
        users_in_room = room.user.all()
    else:
        users_in_room = ""

    context = {'rooms': rooms, 'room_hist': room_hist, 'users_in_room': users_in_room}
    return render(request, 'thegame/rooms.html', context)


@login_required
def new_room(request):
    # Get a 3 digit room number, create database instance, link room to user via foreign key in Room model.
    while True:
        room_num = randint(100, 999)
        # Check to see if that room already exists
        room_check = Room.objects.filter(room_number=room_num)

        if not room_check:
            # Room does not exist. We can break.
            break

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

    # Run a query to see if this room num exists.
    # temp = Room.objects.get(room_number=num)
    try:
        if Room.objects.filter(room_number=num).exists():
            exists = True
        else:
            exists = False
    except ValueError:
        # This likely means they passed through an empty string.
        exists = False

    if not exists:
        # They are trying to join a room that doesnt exist.
        messages.error(request, 'That room does not appear to exist.')
        return redirect('rooms')

    else:
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


@login_required
def delete_unused_rooms(request):
    # remove rooms that are either empty or have no questions associated with them.
    rooms_no_activity = Room.objects.exclude(question__in=Question.objects.all()).exclude(user__in=User.objects.all())

    for room in rooms_no_activity:
        room.delete()

    return redirect('index')


# ***** Testing below this line *****

@login_required
def testing(request):
    # get_unused_rooms(request)

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

    # Users shouldnt be able to be in more than one room at a time... but can they?


def get_unused_rooms(request):
    # rooms = Room.objects.all()
    # users = User.objects.all()
    # user = User.objects.get(username='george')
    # print(rooms)
    # print(users)

    # rooms_no_users = Room.objects.exclude(user__in=User.objects.all())
    # rooms_no_questions = Room.objects.exclude(question__in=Question.objects.all())
    # rooms_no_activity = Room.objects.exclude(question__in=Question.objects.all()).exclude(user__in=User.objects.all())
    # print('rooms_no_users', rooms_no_users)
    # print('rooms_no_questions', rooms_no_questions)
    # print('rooms_no_activity', rooms_no_activity)
    # print(roomss)

    rooms_no_activity = Room.objects.exclude(question__in=Question.objects.all()).exclude(user__in=User.objects.all())

    for room in rooms_no_activity:
        room.delete()
