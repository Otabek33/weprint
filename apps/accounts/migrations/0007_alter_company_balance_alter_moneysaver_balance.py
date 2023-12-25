# Generated by Django 4.2.7 on 2023-12-22 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_moneysaver_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="moneysaver",
            name="balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=20, null=True
            ),
        ),
    ]