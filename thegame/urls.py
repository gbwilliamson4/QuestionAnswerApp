from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views


urlpatterns = [
    # Basic game functionality
    path('', views.index, name='index'),
    path('new-question/', views.new_question, name='new-question'),
    path('save-question/', views.save_question, name='save-question'),
    path('comparing/', views.comparing, name='comparing'),
    path('answers/', views.answers, name='answers'),
    path('answers/<int:question_pk>/', views.save_answer, name='save-answer'),

    # User management.
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Room management
    path('rooms/', views.rooms, name='rooms'),
    path('new-room/', views.new_room, name='new-room'),
    path('leave-room/', views.leave_room, name='leave-room'),
    path('join-room/', views.join_room, name='join-room'),

    # Test page
    path('tests/', views.testing, name='testing'),

    # Admin page for deleting unused rooms
    path('delete-unused-rooms/', views.delete_unused_rooms, name='delete-unused-rooms'),
]