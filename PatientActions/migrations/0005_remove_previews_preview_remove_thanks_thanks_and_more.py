# Generated by Django 4.0.4 on 2022-05-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatientActions', '0004_previews_thanks_delete_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previews',
            name='preview',
        ),
        migrations.RemoveField(
            model_name='thanks',
            name='thanks',
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]