# Generated by Django 2.2 on 2019-11-21 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytic', '0014_auto_20190426_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalreport',
            name='recalculation_total',
            field=models.IntegerField(default=0, verbose_name='Общая сумма перерасчета'),
        ),
        migrations.AddField(
            model_name='violationingeneralreport',
            name='recalculation_total',
            field=models.IntegerField(default=0, verbose_name='Общая сумма перерасчета'),
        ),
    ]
