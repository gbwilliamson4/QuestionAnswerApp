from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class People(models.Model):
    person = models.CharField(max_length=15)

    def __str__(self):
        return self.person


class Answer(models.Model):
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

    class Meta:
        models.UniqueConstraint(fields=['person', 'answer'], name='oneanswerperperson')

    def __str__(self):
        return self.answer

# class GeorgeAnswer(models.Model):
#     question = models.OneToOneField(Question, on_delete=models.CASCADE)
#     answer = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.answer
#
#
# class KelsyAnswer(models.Model):
#     question = models.OneToOneField(Question, on_delete=models.CASCADE)
#     answer = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.answer
