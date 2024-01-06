from django.urls import reverse
from datetime import datetime
from django.db import models
from apps.accounts.models import CustomUser, Company
from django.utils.translation import gettext_lazy as _
import uuid

from apps.tg.models import PrintSize, PrintColor
from apps.orders.models import PrintBindingTypes


# Create your models here.
class ProductManager(models.Manager):
    """nimadur"""

    def by_creator(self, user):
        return super().get_queryset().filter(deleted_status=False, created_by=user).order_by('-created_at')

    def by_id(self, id):
        return super().get_queryset().get(pk=id)

    def get_product(self, color, size, binding):
        return super().get_queryset().get(printColor=color, printSize=size, printBindingType=binding)


# Create your models here.
class Product(models.Model):
    """mahsulot"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    printSize = models.IntegerField(
        choices=PrintSize.choices,
        default=PrintSize.A5,
    )
    printColor = models.IntegerField(
        choices=PrintColor.choices,
        default=PrintColor.WHITE,
    )
    printBindingType = models.ForeignKey(PrintBindingTypes,
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True,
                                         related_name="printBindingTypess", )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name="company", )



    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Size - {self.get_printSize_display()} \n; Color - {self.get_printColor_display()} ; Binding  - {self.printBindingType.name} ; Price  - {str(self.price)};"

    def get_absolute_url(self):
        return reverse("products:product_list")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
