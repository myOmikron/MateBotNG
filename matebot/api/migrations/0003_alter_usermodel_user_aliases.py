# Generated by Django 4.0 on 2021-12-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_application_applicationmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_aliases',
            field=models.ManyToManyField(blank=True, to='api.UserAliasModel'),
        ),
    ]
