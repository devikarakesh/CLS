# Generated by Django 5.1.1 on 2025-02-13 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0022_alter_userprofile_status_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'student'), ('FACULTY', 'Faculty'), ('ADMIN', 'Admin'), ('LABSTAFF', 'Labstaff')], max_length=20),
        ),
    ]
