import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser


# Create your models here.
class Client(models.Model):
    """Class representing a person"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.CharField(_("Chat id"), max_length=13, null=True, blank=True)
    phone = models.CharField(_("Telefon"), max_length=13, blank=True, null=True)
    username = models.CharField(
        _("Username"),
        max_length=150,
    )
    first_name = models.CharField(_("Ism"), max_length=150, blank=True)
    last_name = models.CharField(_("Familiya"), max_length=150, blank=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="client_created_by",
    )
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="client_updated_by",
    )
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), blank=True, null=True)
    deleted_status = models.BooleanField(_("O'chirilganlik statusi"), default=False)
    total_debit = models.DecimalField(
        _("Umumiy debit"), max_digits=20, decimal_places=2, default=0
    )
    total_credit = models.DecimalField(
        _("Umumiy kredit"), max_digits=20, decimal_places=2, default=0
    )
    balance = models.DecimalField(
        _("Balans"), max_digits=20, decimal_places=2, default=0
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("clients:client_list")

    class Meta:
        """Class representing a client"""

        verbose_name = _("Mijoz")
        verbose_name_plural = _("Mijozlar")
