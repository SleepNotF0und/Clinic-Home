# Generated by Django 4.0.4 on 2022-05-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_rename_insurance_companies_doctors_insurance_company1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctors',
            name='dateofbirth',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='info',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='specialize',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]