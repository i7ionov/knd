# Generated by Django 2.1.4 on 2019-03-18 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0005_auto_20190315_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='adrecord',
            name='datetime_of_trial',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время рассмотрения'),
        ),
        migrations.AddField(
            model_name='historicaladrecord',
            name='datetime_of_trial',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время рассмотрения'),
        ),
    ]