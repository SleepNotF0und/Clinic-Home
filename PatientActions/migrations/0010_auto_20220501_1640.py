# Generated by Django 3.2.12 on 2022-05-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatientActions', '0009_reservations_opptdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]