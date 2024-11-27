# Generated by Django 5.1.1 on 2024-11-27 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_rename_teacher_timetableentry1_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.lab')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_start_time', models.TimeField()),
                ('slot_end_time', models.TimeField()),
                ('working_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.workingday')),
            ],
        ),
    ]
