# Generated by Django 4.2.7 on 2023-12-27 06:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tg", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="chat",
        ),
        migrations.DeleteModel(
            name="Chat",
        ),
        migrations.DeleteModel(
            name="Theme",
        ),
    ]