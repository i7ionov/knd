# Generated by Django 2.1.4 on 2019-03-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0016_auto_20190314_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='ФИО')),
                ('organizations', models.ManyToManyField(blank=True, to='dictionaries.Organization', verbose_name='Организации')),
            ],
        ),
    ]