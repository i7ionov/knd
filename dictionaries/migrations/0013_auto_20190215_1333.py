# Generated by Django 2.1.4 on 2019-02-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0012_auto_20190214_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhouse',
            name='living_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь жилых помещений'),
        ),
        migrations.AlterField(
            model_name='historicalhouse',
            name='non_living_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь нежилых помещений'),
        ),
        migrations.AlterField(
            model_name='historicalhouse',
            name='total_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь'),
        ),
        migrations.AlterField(
            model_name='house',
            name='living_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь жилых помещений'),
        ),
        migrations.AlterField(
            model_name='house',
            name='non_living_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь нежилых помещений'),
        ),
        migrations.AlterField(
            model_name='house',
            name='total_area',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='общая площадь'),
        ),
    ]
