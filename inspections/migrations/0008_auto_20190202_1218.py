# Generated by Django 2.1.4 on 2019-02-02 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0007_auto_20190129_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspection',
            options={'permissions': (('can_change_others_inspections', 'Сan change others inspections'),), 'verbose_name': 'Проверка'},
        ),
    ]