# Generated by Django 4.2.7 on 2024-01-03 09:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0009_alter_transaction_cash_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="transaction",
            options={
                "verbose_name": "Tranzaksiya",
                "verbose_name_plural": "Tranzaksiyalar",
            },
        ),
    ]
