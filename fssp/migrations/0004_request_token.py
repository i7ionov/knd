# Generated by Django 2.2 on 2021-04-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fssp', '0003_request_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='token',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
