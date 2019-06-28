# Generated by Django 2.2 on 2019-04-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0011_auto_20190416_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinspection',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='violationtype',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='violationtype',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='violationtype',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]