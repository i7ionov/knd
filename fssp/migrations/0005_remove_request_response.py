# Generated by Django 2.2 on 2021-04-26 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fssp', '0004_request_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='response',
        ),
    ]