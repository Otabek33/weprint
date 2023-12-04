from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from apps.tg.models import PrintColor, PrintSize, PrintBindingTypes


# Create your models here.
class OrderStatus(models.IntegerChoices):
    CREATION = 1, _("В создании")
    CONFORM = 2, _("В подтверждении")
    ACTIVE = 3, _("Активный")
    CANCELLED = 4, _("Отменено")


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.IntegerField(default=0)
    printSize = models.IntegerField(
        choices=PrintSize.choices,
        default=PrintSize.A4,
    )
    printColor = models.IntegerField(
        choices=PrintColor.choices,
        default=PrintColor.WHITE,
    )
    printBindingType = models.IntegerField(
        choices=PrintBindingTypes.choices,
        default=PrintBindingTypes.NO_BINDING,
    )
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    page_number = models.IntegerField()
    order_status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.CREATION,
    )
    created_by = models.ForeignKey("clients.Client", verbose_name=_("Created by"), on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name="order_created_by")
    updated_by = models.ForeignKey("clients.Client", verbose_name=_("Updated by"), on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name="order_updated_by")
    created_at = models.DateTimeField

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
