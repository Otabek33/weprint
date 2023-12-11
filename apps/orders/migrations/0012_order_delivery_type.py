# Generated by Django 4.2.7 on 2023-12-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0011_order_cash_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_type",
            field=models.IntegerField(
                choices=[(1, "O'zim olib ketaman"), (2, "Kuryerlik xizmati")], default=1
            ),
        ),
    ]
