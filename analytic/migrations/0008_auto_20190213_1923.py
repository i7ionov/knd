# Generated by Django 2.1.4 on 2019-02-13 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytic', '0007_abstractitemcountinreport_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalreport',
            name='violation_count',
            field=models.IntegerField(default=0, verbose_name='Количество выявленных нарушений'),
        ),
        migrations.AddField(
            model_name='generalreport',
            name='violations_count_of_removed',
            field=models.IntegerField(default=0, verbose_name='Количество устраненных нарушений'),
        ),
        migrations.AddField(
            model_name='generalreport',
            name='violations_count_to_remove',
            field=models.IntegerField(default=0, verbose_name='Количество нарушений к устранению'),
        ),
    ]