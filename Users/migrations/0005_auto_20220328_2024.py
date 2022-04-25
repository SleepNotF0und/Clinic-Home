# Generated by Django 3.0.4 on 2022-03-28 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_customuser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
