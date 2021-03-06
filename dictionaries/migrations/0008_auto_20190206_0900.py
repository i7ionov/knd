# Generated by Django 2.1.4 on 2019-02-06 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0007_auto_20190130_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('name_rp', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='department',
            new_name='department_old',
        ),
        migrations.AddField(
            model_name='historicalhouse',
            name='building_year',
            field=models.IntegerField(blank=True, default=0, verbose_name='год постройки'),
        ),
        migrations.AddField(
            model_name='historicalhouse',
            name='living_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь жилых помещений'),
        ),
        migrations.AddField(
            model_name='historicalhouse',
            name='non_living_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь нежилых помещений'),
        ),
        migrations.AddField(
            model_name='historicalhouse',
            name='number_of_apartments',
            field=models.IntegerField(blank=True, default=0, verbose_name='количество квартир'),
        ),
        migrations.AddField(
            model_name='historicalhouse',
            name='total_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь'),
        ),
        migrations.AddField(
            model_name='house',
            name='building_year',
            field=models.IntegerField(blank=True, default=0, verbose_name='год постройки'),
        ),
        migrations.AddField(
            model_name='house',
            name='living_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь жилых помещений'),
        ),
        migrations.AddField(
            model_name='house',
            name='non_living_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь нежилых помещений'),
        ),
        migrations.AddField(
            model_name='house',
            name='number_of_apartments',
            field=models.IntegerField(blank=True, default=0, verbose_name='количество квартир'),
        ),
        migrations.AddField(
            model_name='house',
            name='total_area',
            field=models.IntegerField(blank=True, default=0, verbose_name='общая площадь'),
        ),
        migrations.AlterField(
            model_name='house',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dictionaries.Organization', verbose_name='Организация'),
        ),
    ]
