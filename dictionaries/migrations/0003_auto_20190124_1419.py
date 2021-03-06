# Generated by Django 2.1.4 on 2019-01-24 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0002_auto_20190117_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='files',
            field=models.ManyToManyField(blank=True, to='dictionaries.File', verbose_name='файлы'),
        ),
        migrations.AlterField(
            model_name='document',
            name='houses',
            field=models.ManyToManyField(blank=True, to='dictionaries.House', verbose_name='адреса домов'),
        ),
        migrations.AlterField(
            model_name='document',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionaries.Organization', verbose_name='Организация'),
        ),
    ]
