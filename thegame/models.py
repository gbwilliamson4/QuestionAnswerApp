from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_number = models.IntegerField()
    user = models.ManyToManyField(User, default=None, blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['room_number', 'user'], name='one room at a time per user')
    #     ]

    def __str__(self):
        return str(self.room_number)


class Question(models.Model):
    question = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class People(models.Model):
    person = models.CharField(max_length=15)

    def __str__(self):
        return self.person


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer', 'question'], name='one answer per user per question')
        ]

    def __str__(self):
        return self.answer


class Room_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name='one log or something')
        ]
