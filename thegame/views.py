from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from random import randint # Used for generating random 3 digit room numbers.


# def index(request):
#     return HttpResponse("Welcome to the index page.")

def index(request):
    context = {}
    return render(request, 'thegame/index.html', context)

# This one is the original.
# def new_question(request):
#     """Add a new question."""
#     questions = Question.objects.all()
#     # questions = Question.objects.filter(room=request.user.room)
#     if request.method != 'POST':
#         # No data submitted; create a blank form.
#         form = QuestionForm()
#     else:
#         # POST data submitted; process data.
#         form = QuestionForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('new_question')
#
#     # Display a blank or invalid form.
#     context = {'form': form, 'questions': questions}
#     return render(request, 'thegame/new-question.html', context)

def new_question(request):
    """Add a new question."""
    # Get room num and questions in that room.
    room_num = request.user.room_set.first()
    room_num_id = room_num.pk
    questions = Question.objects.filter(room=room_num_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = QuestionForm()
    else:
        # POST data submitted; process data.
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('new-question')

    # Display a blank or invalid form.
    context = {'form': form, 'questions': questions}
    return render(request, 'thegame/new-question.html', context)

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


def new_answers(request):
    # Get room num and questions in that room.
    room_num = request.user.room_set.first()
    room_num_id = room_num.pk
    questions = Question.objects.filter(room=room_num_id)

    context = {'questions': questions}
    return render(request, 'thegame/answers.html', context)


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

    return redirect('answers')


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
            return redirect('index')
    else:
        return render(request, 'thegame/login.html', {})

@login_required
def rooms(request):
    rooms = Room.objects.filter(user=request.user)
    context = {'rooms': rooms}
    return render(request, 'thegame/rooms.html', context)

@login_required
def new_room(request):
    room_num = randint(100, 999)
    room = Room(room_number=room_num)
    room.save()
    room.user.add(request.user)
    room.save()
    return redirect('rooms')


@login_required
def leave_room(request):
    print('attempting to leave room')
    room = Room.objects.filter(user=request.user)
    room = room[0]
    room.user.remove(request.user)
    room.save()
    return redirect('rooms')

@login_required
def join_room(request):
    num = request.POST['room-num']
    num = int(num) # make sure that its an integer.
    print(request.user)
    user = request.user
    room = Room.objects.filter(room_number=num)
    room = room[0]
    room.user.add(user)
    room.save()

    return redirect('rooms')
