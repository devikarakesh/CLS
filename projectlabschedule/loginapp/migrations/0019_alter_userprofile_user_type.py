# Generated by Django 5.1.1 on 2024-12-31 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0018_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'student'), ('LABSTAFF', 'Labstaff'), ('ADMIN', 'Admin'), ('FACULTY', 'Faculty')], max_length=20),
        ),
    ]
