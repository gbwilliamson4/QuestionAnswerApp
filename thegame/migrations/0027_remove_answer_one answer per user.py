# Generated by Django 4.1.2 on 2022-10-07 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thegame', '0026_answer_one answer per user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='answer',
            name='one answer per user',
        ),
    ]
