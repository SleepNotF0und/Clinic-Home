# Generated by Django 3.0.4 on 2022-03-30 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0013_auto_20220330_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(max_length=20, null=True),
        ),
    ]