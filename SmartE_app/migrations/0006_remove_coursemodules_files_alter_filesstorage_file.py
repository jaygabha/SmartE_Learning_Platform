# Generated by Django 4.2.1 on 2023-07-21 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartE_app', '0005_alter_professor_options_alter_student_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemodules',
            name='files',
        ),
        migrations.AlterField(
            model_name='filesstorage',
            name='file',
            field=models.FileField(upload_to='module/course_files'),
        ),
    ]
