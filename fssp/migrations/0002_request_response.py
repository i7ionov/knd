# Generated by Django 2.2 on 2021-04-23 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fssp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='response',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fssp.Response'),
        ),
    ]
