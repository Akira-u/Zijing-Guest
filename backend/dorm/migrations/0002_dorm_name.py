# Generated by Django 3.2.9 on 2021-12-09 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dorm',
            name='name',
            field=models.CharField(default='empty', max_length=20),
        ),
    ]
