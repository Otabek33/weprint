# Generated by Django 4.2.4 on 2024-01-23 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_clientaddress_unique_together'),
        ('orders', '0004_order_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.clientaddress'),
        ),
    ]
