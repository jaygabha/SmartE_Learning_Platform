# Generated by Django 4.2.1 on 2023-07-20 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SmartE_app", "0004_coursemodules_files"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="professor",
            options={"verbose_name": "Professor"},
        ),
        migrations.AlterModelOptions(
            name="student",
            options={"verbose_name": "Student"},
        ),
    ]
