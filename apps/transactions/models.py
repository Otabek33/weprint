from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser
from apps.clients.models import Client
from apps.products.models import Product


# Create your models here.

class CashType(models.IntegerChoices):
    CASH = 1, _('Naqt')
    BANK = 2, _('Bank')
    PRODUCT = 3, _('Mahsulot')


class DoubleEntryAccounting(models.IntegerChoices):
    CREDIT = 1, _('Kredit')
    DEBIT = 2, _('Debit')


class Transaction(models.Model):
    """Class representing a person"""

    description = models.CharField("Ta'rif", blank=True, max_length=55)
    cash_type = models.IntegerField("Pul turi",
                                    choices=CashType.choices,
                                    default=CashType.CASH)
    client = models.ForeignKey(Client,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               related_name="client_transaction", )
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name="product_transaction", )
    double_entry_accounting = models.IntegerField("Pul yo'nalishi",
                                                  choices=DoubleEntryAccounting.choices,
                                                  default=DoubleEntryAccounting.CREDIT)
    balance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transaction_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transaction_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)

    class Meta:
        """Class representing a person"""
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакция"

    def __str__(self) -> str:
        return str(self.description)