# Generated by Django 5.1.1 on 2024-10-10 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
