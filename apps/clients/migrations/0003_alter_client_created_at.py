# Generated by Django 4.2.7 on 2024-01-10 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0002_alter_client_options_alter_client_balance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Yaratilgan vaqt"
            ),
        ),
    ]