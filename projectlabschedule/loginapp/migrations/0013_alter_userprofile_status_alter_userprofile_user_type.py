# Generated by Django 5.1.1 on 2024-10-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0012_alter_userprofile_status_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('DEACTIVE', 'Deactive')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'student'), ('FACULTY', 'Faculty'), ('ADMIN', 'Admin'), ('LABSTAFF', 'Labstaff')], max_length=20),
        ),
    ]
