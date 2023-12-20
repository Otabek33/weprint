# Generated by Django 4.2.7 on 2023-12-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="cash_type",
            field=models.IntegerField(
                choices=[(1, "Naqt"), (2, "Karta orqali"), (3, "To'lanmadi")], default=3
            ),
        ),
    ]