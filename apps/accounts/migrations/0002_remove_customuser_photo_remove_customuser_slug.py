# Generated by Django 4.2.7 on 2023-12-01 04:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="slug",
        ),
    ]