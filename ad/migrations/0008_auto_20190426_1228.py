# Generated by Django 2.2 on 2019-04-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0007_auto_20190328_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaladrecord',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicaladrecord',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicaladrecord',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalexecution',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalexecution',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalexecution',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]