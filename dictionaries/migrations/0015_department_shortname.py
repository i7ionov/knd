# Generated by Django 2.1.4 on 2019-03-14 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0014_auto_20190222_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='shortname',
            field=models.CharField(default='', max_length=200, verbose_name='отдел'),
            preserve_default=False,
        ),
    ]
