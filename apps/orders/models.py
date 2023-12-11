from django.utils import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from apps.tg.models import PrintColor, PrintSize


# Create your models here.
class OrderStatus(models.IntegerChoices):
    CREATION = 1, _("Yangi")
    ORDERD = 2, _("Buyurtma berilgan")
    ACTIVE = 3, _("Faol")
    CANCELLED = 4, _("Bekor qilingan")
    FINISH = 5, _("Yetqazib berilgan")


class PrintBindingTypes(models.Model):
    name = models.CharField(_("Nomi"), max_length=150, blank=True)
    photo = models.FileField(upload_to="binding/%Y/%m/%d/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Binding type"
        verbose_name_plural = "Biding types"


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(_("Buyurtma raqami"), max_length=150, blank=True)
    printSize = models.IntegerField(
        choices=PrintSize.choices,
        default=PrintSize.A4,
    )
    printColor = models.IntegerField(
        choices=PrintColor.choices,
        default=PrintColor.WHITE,
    )
    printBindingType = models.ForeignKey(PrintBindingTypes,
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True,
                                         related_name="printBindingTypes", )
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    page_number = models.IntegerField(default=0)
    order_status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.CREATION,
    )
    created_by = models.ForeignKey("clients.Client", verbose_name=_("Created by"), on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name="order_created_by")
    updated_by = models.ForeignKey("clients.Client", verbose_name=_("Updated by"), on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name="order_updated_by")
    created_at = models.DateTimeField(default=timezone.now)
    tg_pk = models.CharField(max_length=150, default=0)
    file_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
