# Generated by Django 4.2.1 on 2023-07-23 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SmartE_app', '0013_moduleprogress_delete_moduleprogresstracker_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='students',
        ),
    ]