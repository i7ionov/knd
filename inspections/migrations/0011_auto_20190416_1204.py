# Generated by Django 2.1.4 on 2019-04-16 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0010_auto_20190328_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprecept',
            name='days_to_start_new_inspection',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дней до запуска проверки'),
        ),
        migrations.AddField(
            model_name='precept',
            name='days_to_start_new_inspection',
            field=models.IntegerField(blank=True, null=True, verbose_name='Дней до запуска проверки'),
        ),
    ]
