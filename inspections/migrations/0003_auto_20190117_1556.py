# Generated by Django 2.1.4 on 2019-01-17 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0002_auto_20190117_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinspection',
            name='doc_date',
            field=models.DateField(blank=True, verbose_name='дата документа'),
        ),
        migrations.AlterField(
            model_name='historicalorder',
            name='doc_date',
            field=models.DateField(blank=True, verbose_name='дата документа'),
        ),
    ]