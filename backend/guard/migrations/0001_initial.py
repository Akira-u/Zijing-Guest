# Generated by Django 3.2.9 on 2021-12-14 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dorm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guard',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('open_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=15)),
                ('dormbuilding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Guard_Dorm_Building', to='dorm.dormbuilding')),
            ],
        ),
    ]
