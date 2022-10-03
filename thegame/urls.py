from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new_question/', views.new_question, name='new_question'),
    path('comparing/', views.comparing, name='comparing'),
    path('george_answers/', views.george_answers, name='george_answers'),
    path('kelsy_answers/', views.kelsy_answers, name='kelsy_answers'),
    path('george_answers/<int:question_pk>/', views.save_g_answer, name='save_g_answer'),
]