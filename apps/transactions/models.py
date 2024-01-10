from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser, Company, MoneySaver
from apps.clients.models import Client
from apps.orders.models import Order
from apps.products.models import Product


# Create your models here.


class DoubleEntryAccounting(models.IntegerChoices):
    CREDIT = 1, _('Kredit')
    DEBIT = 2, _('Debit')


class Transaction(models.Model):
    """Transaction"""
    payment_order = models.IntegerField(_("To'lov raqami"), blank=True, null=True)

    description = models.CharField(_("Ta'rif"), blank=True, max_length=55)
    cash_type = models.ForeignKey(MoneySaver, blank=True, null=True, on_delete=models.CASCADE, )
    client = models.ForeignKey(Client,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               related_name="client_transaction", )
    order = models.ForeignKey(Order,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name="order_transaction", )
    double_entry_accounting = models.IntegerField(_("Pul yo'nalishi"),
                                                  choices=DoubleEntryAccounting.choices,
                                                  default=DoubleEntryAccounting.CREDIT)
    balance = models.DecimalField(_("Balans"), max_digits=20, decimal_places=2, default=0)
    company_balance = models.DecimalField(_("Korxona balansi"), max_digits=20, decimal_places=2, default=0)
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name="company_transaction", )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transaction_created_by",
    )
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="transaction_updated_by",
    )
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), blank=True, null=True)
    deleted_status = models.BooleanField(_("O'chirilganlik status"), default=False)

    class Meta:
        """Class representing a transaction"""
        verbose_name = _("Tranzaksiya")
        verbose_name_plural = _("Tranzaksiyalar")

    def __str__(self) -> str:
        return str(self.description)
