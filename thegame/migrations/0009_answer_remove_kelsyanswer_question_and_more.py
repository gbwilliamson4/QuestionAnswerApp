# Generated by Django 4.1.1 on 2022-10-04 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thegame', '0008_alter_kelsyanswer_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thegame.people')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thegame.question')),
            ],
        ),
        migrations.RemoveField(
            model_name='kelsyanswer',
            name='question',
        ),
        migrations.DeleteModel(
            name='GeorgeAnswer',
        ),
        migrations.DeleteModel(
            name='KelsyAnswer',
        ),
    ]