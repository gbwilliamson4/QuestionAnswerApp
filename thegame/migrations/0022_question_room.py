# Generated by Django 4.1.2 on 2022-10-06 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thegame', '0021_remove_question_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='room',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='thegame.room'),
        ),
    ]
