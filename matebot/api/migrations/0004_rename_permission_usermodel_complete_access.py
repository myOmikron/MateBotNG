# Generated by Django 4.0 on 2021-12-27 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_usermodel_user_aliases'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='permission',
            new_name='complete_access',
        ),
    ]