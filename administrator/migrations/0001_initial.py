# Generated by Django 5.1.1 on 2024-09-25 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=200, null=True)),
                ('notificationdate', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
