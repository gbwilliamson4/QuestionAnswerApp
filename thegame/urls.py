from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views


urlpatterns = [
    # Basic game functionality
    path('', views.new_question, name='index'),
    path('new_question/', views.new_question, name='new_question'),
    path('comparing/', views.comparing, name='comparing'),
    path('george_answers/', views.george_answers, name='george_answers'),
    path('kelsy_answers/', views.kelsy_answers, name='kelsy_answers'),
    path('answers/<int:question_pk>/<str:person>', views.save_answer, name='save-answer'),

    # User management.
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Room management
    path('rooms/', views.rooms, name='rooms'),
    path('new-room/', views.new_room, name='new-room'),
    path('leave-room/', views.leave_room, name='leave-room'),
    path('join-room/', views.join_room, name='join-room'),
]