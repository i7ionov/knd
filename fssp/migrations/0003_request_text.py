# Generated by Django 2.2 on 2021-04-26 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fssp', '0002_request_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
