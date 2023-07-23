# Generated by Django 4.2.2 on 2023-07-16 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SmartE_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="expiry_date",
        ),
        migrations.AlterField(
            model_name="membership",
            name="type",
            field=models.CharField(
                choices=[("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold")],
                max_length=20,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]