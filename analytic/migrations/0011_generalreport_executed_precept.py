# Generated by Django 2.1.4 on 2019-03-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytic', '0010_auto_20190223_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalreport',
            name='executed_precept',
            field=models.IntegerField(default=0, verbose_name='Количество исполненных предписаний'),
        ),
    ]