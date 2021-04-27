# Generated by Django 2.2 on 2021-04-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('type', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('exe_production', models.TextField()),
                ('details', models.TextField()),
                ('subject', models.TextField()),
                ('department', models.TextField()),
                ('bailiff', models.TextField()),
                ('ip_end', models.TextField()),
            ],
        ),
    ]
