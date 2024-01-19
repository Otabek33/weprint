import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import ClientAddress, Company
from apps.products.models import PrintBindingTypes
from apps.tg.models import DeliveryType, PaymentType, PrintColor, PrintSize


# Create your models here.
class OrderStatus(models.IntegerChoices):
    CREATION = 1, _("Yaratilish")
    ORDERED = 2, _("Yangi Buyurtma")
    ACTIVE = 3, _("Faol")
    CANCELLED = 4, _("Bekor qilingan")
    FINISH = 5, _("Yetqazib berilgan")


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(_("Buyurtma raqami"), max_length=150, blank=True)
    printSize = models.IntegerField(
        _("Hajmi"),
        choices=PrintSize.choices,
        default=PrintSize.A4,
    )
    printColor = models.IntegerField(
        _("Rang"),
        choices=PrintColor.choices,
        default=PrintColor.WHITE,
    )
    printBindingType = models.ForeignKey(
        PrintBindingTypes,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="printBindingTypes",
    )
    file = models.FileField(_("Fayl"), upload_to="uploads/%Y/%m/%d/", blank=True, null=True)
    price = models.DecimalField(_("Narx"), max_digits=20, decimal_places=2, default=0.0)
    total_debit = models.DecimalField(
        _("Umumiy debit"), max_digits=20, decimal_places=2, default=0
    )
    total_credit = models.DecimalField(
        _("Umumiy kredit"), max_digits=20, decimal_places=2, default=0
    )
    balance = models.DecimalField(
        _("Balans"), max_digits=20, decimal_places=2, default=0
    )
    page_number = models.IntegerField(_("Sahifa soni"), default=0)
    order_status = models.IntegerField(
        _("Buyurtma statusi"),
        choices=OrderStatus.choices,
        default=OrderStatus.CREATION,
    )
    created_by = models.ForeignKey(
        "clients.Client",
        verbose_name=_("Created by"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order_created_by",
    )
    updated_by = models.ForeignKey(
        "clients.Client",
        verbose_name=_("Updated by"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order_updated_by",
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name="company_order", )
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), default=timezone.now)
    tg_pk = models.CharField(_("Telegram id"), max_length=150, default=0)
    file_status = models.BooleanField(_("Fayl statusi"), default=False)
    cash_type = models.IntegerField(
        _("Pul turi"),
        choices=PaymentType.choices,
        default=PaymentType.WAIT,
    )
    delivery_type = models.IntegerField(
        _("Yetqazib berish turi"),
        choices=DeliveryType.choices,
        default=DeliveryType.Self_Delivery,
    )
    location = models.OneToOneField(ClientAddress, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")
