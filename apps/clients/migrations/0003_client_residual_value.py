# Generated by Django 4.2.7 on 2023-12-26 04:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0002_client_order_amount_client_total_credit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="residual_value",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=20, null=True
            ),
        ),
    ]
