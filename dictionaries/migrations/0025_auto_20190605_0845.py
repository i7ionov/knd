# Generated by Django 2.2 on 2019-06-05 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0024_auto_20190429_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionaries.OrganizationType', verbose_name='Тип организации'),
        ),
    ]