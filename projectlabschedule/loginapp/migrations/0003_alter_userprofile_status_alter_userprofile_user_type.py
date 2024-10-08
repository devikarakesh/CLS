# Generated by Django 5.1.1 on 2024-09-18 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0002_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('DEACTIVE', 'Deactive'), ('ACTIVE', 'Active')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'Student'), ('FACULTY', 'Faculty'), ('LABSTAFF', 'Labstaff'), ('ADMIN', 'Admin')], max_length=20),
        ),
    ]
