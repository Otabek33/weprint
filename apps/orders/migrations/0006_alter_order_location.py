# Generated by Django 4.2.7 on 2024-01-01 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0005_alter_order_residual_value_alter_order_total_credit_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="location",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.clientaddress",
            ),
        ),
    ]