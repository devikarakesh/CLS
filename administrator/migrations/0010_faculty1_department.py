# Generated by Django 5.1.1 on 2025-02-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0009_labstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty1',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
