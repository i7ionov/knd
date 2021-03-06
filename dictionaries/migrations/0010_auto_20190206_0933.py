# Generated by Django 2.1.4 on 2019-02-06 04:33

from django.db import migrations


def create_departments(apps, schema_editor):
    User = apps.get_model('dictionaries', 'User')
    Department = apps.get_model('dictionaries', 'Department')
    for u in User.objects.all():
        d, created = Department.objects.get_or_create(name=u.department_old)
        u.department = d
        u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0009_auto_20190206_0928'),
    ]

    operations = [
        migrations.RunPython(create_departments),
    ]
