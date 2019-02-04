# Generated by Django 2.1.4 on 2019-01-30 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0005_auto_20190130_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhouse',
            name='comment',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='comment',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]