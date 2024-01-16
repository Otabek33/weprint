# Generated by Django 4.2.7 on 2024-01-10 09:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_printbindingtypes_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="printbindingtypes",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Yaratilgan vaqt"
            ),
        ),
        migrations.AlterField(
            model_name="printbindingtypes",
            name="deleted_status",
            field=models.BooleanField(
                default=False, verbose_name="O'chirilganlik statusi"
            ),
        ),
        migrations.AlterField(
            model_name="printbindingtypes",
            name="photo",
            field=models.ImageField(upload_to="binding/%Y/%m/%d/", verbose_name="Rasm"),
        ),
        migrations.AlterField(
            model_name="printbindingtypes",
            name="updated_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="O'zgartirilgan vaqt"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="Yaratilgan vaqt"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="deleted_status",
            field=models.BooleanField(
                default=False, verbose_name="O'chirilganlik statusi"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=10, verbose_name="Narx"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="printColor",
            field=models.IntegerField(
                choices=[(1, "Oq qora"), (2, "Rangli")], default=1, verbose_name="Rang"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="printSize",
            field=models.IntegerField(
                choices=[(1, "A5"), (2, "A4")], default=1, verbose_name="Hajm"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="O'zgartirilgan vaqt"
            ),
        ),
    ]