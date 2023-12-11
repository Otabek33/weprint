# Generated by Django 4.2.7 on 2023-12-11 13:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clients", "0003_alter_client_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="some place", max_length=255)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrintBindingTypes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=150, verbose_name="Nomi"),
                ),
                ("photo", models.FileField(upload_to="binding/%Y/%m/%d/")),
            ],
            options={
                "verbose_name": "Binding type",
                "verbose_name_plural": "Biding types",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "order_number",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Buyurtma raqami"
                    ),
                ),
                (
                    "printSize",
                    models.IntegerField(choices=[(1, "A5"), (2, "A4")], default=2),
                ),
                (
                    "printColor",
                    models.IntegerField(
                        choices=[(1, "Oq qora"), (2, "Rangli")], default=1
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/%Y/%m/%d/")),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("page_number", models.IntegerField(default=0)),
                (
                    "order_status",
                    models.IntegerField(
                        choices=[
                            (1, "Yaratilish"),
                            (2, "Yangi Buyurtma"),
                            (3, "Faol"),
                            (4, "Bekor qilingan"),
                            (5, "Yetqazib berilgan"),
                        ],
                        default=1,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("tg_pk", models.CharField(default=0, max_length=150)),
                ("file_status", models.BooleanField(default=False)),
                (
                    "cash_type",
                    models.IntegerField(
                        choices=[(1, "Naqt"), (2, "Karta orqali")], default=1
                    ),
                ),
                (
                    "delivery_type",
                    models.IntegerField(
                        choices=[(1, "O'zim olib ketaman"), (2, "Kuryerlik xizmati")],
                        default=1,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order_created_by",
                        to="clients.client",
                        verbose_name="Created by",
                    ),
                ),
                (
                    "location",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.location",
                    ),
                ),
                (
                    "printBindingType",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="printBindingTypes",
                        to="orders.printbindingtypes",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order_updated_by",
                        to="clients.client",
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
    ]
