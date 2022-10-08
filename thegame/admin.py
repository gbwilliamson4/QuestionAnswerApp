from django.contrib import admin
from .models import *


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]


class UserInLine(admin.StackedInline):
    model = Room.user.through
    extra = 3


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5


class RoomAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine, UserInLine]
    exclude = ['user']


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ('answer', 'question', 'user')


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Room, RoomAdmin)
