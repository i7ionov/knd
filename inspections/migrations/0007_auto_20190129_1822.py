# Generated by Django 2.1.4 on 2019-01-29 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0006_auto_20190128_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinspection',
            name='cancellation',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.Cancellation', verbose_name='Информация об отмене результатов проверки'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='control_form',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.ControlForm', verbose_name='форма проверки'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='control_kind',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.ControlKind', verbose_name='вид контроля'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='control_plan',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.ControlPlan', verbose_name='вид проверки'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='document_ptr',
            field=models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='dictionaries.Document'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='inspection_result',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.InspectionResult', verbose_name='Результат проверки'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='inspector',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dictionaries.User', verbose_name='инспектор'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='legal_basis',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.LegalBasis', verbose_name='основание для проверки'),
        ),
        migrations.AlterField(
            model_name='historicalinspection',
            name='organization',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dictionaries.Organization', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='document_ptr',
            field=models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='dictionaries.Document'),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='organization',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dictionaries.Organization', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='historicalprecept',
            name='precept_result',
            field=models.ForeignKey(blank=True, db_constraint=False, default='1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inspections.PreceptResult', verbose_name='результат предписания'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='inspection_result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inspections.InspectionResult', verbose_name='Результат проверки'),
        ),
    ]
