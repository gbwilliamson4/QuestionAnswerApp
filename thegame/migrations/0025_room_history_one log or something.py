# Generated by Django 4.1.2 on 2022-10-07 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thegame', '0024_room_history'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='room_history',
            constraint=models.UniqueConstraint(fields=('user', 'room'), name='one log or something'),
        ),
    ]
