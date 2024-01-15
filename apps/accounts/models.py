import uuid as uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CashType(models.IntegerChoices):
    CASH = 1, _("Naqt")
    BANK = 2, _("Bank")


class UserRole(models.Model):
    """Class representing a person"""

    name = models.CharField(_("Nomlanishi"), blank=True, max_length=55)
    code = models.CharField(_("Kod"), max_length=55)

    class Meta:
        """Class representing a person"""

        verbose_name = _("Foydaluvchilar turi")
        verbose_name_plural = _("Foydaluvchilar turlari")

    def __str__(self) -> str:
        return str(self.name)


class ClientAddress(models.Model):
    name = models.CharField(_("Nomi"), max_length=255, default="some place")
    latitude = models.DecimalField(
        _("Latitude"), max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        _("Longitude"), max_digits=9, decimal_places=6, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    """Class representing a person"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Nomi"), blank=True, max_length=55)
    email = models.EmailField(_("Pochta"), max_length=100, null=True, blank=True)
    phone = models.CharField(_("Telefon"), max_length=100, null=True, blank=True)
    balance = models.DecimalField(
        _("Balans"), max_digits=20, decimal_places=2, default=0
    )
    total_debit = models.DecimalField(
        _("Umumiy deit"), max_digits=20, decimal_places=2, default=0
    )
    total_credit = models.DecimalField(
        _("Umumiy kredit"), max_digits=20, decimal_places=2, default=0
    )
    location = models.OneToOneField(
        ClientAddress,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="company_address",
    )

    class Meta:
        """Class representing a person"""

        verbose_name = _("Kompaniya")
        verbose_name_plural = _("Kompaniyalar")

    def __str__(self) -> str:
        return str(self.name)


class CustomUser(AbstractUser):
    """Class representing a person"""

    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Foydanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    # def get_absolute_url(self):
    #     return reverse("accounts:user-detail", kwargs={"pk": self.id})
    @property
    def is_user(self):
        return self.role.name == "user"

    @property
    def is_admin(self):
        """Class representing a person"""
        return self.role.name == "admin"

    @property
    def is_super_user(self):
        """Class representing a person"""
        return self.role.name == "superuser"


class MoneySaver(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reester_number = models.CharField(_("Reyester"), blank=True, max_length=55)
    cashType = models.IntegerField(
        _("Pul turi"), choices=CashType.choices, default=CashType.CASH
    )
    balance = models.DecimalField(
        _("Balans"), max_digits=20, decimal_places=2, default=0
    )
    total_debit = models.DecimalField(
        _("Umumiy debit"), max_digits=20, decimal_places=2, default=0
    )
    total_credit = models.DecimalField(
        _("Umumiy kredit"), max_digits=20, decimal_places=2, default=0
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_moneySaver",
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="bank_created_by",
    )
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="bank_updated_by",
    )
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), blank=True, null=True)
    deleted_status = models.BooleanField(_("O'chirilganlik statusi"), default=False)

    class Meta:
        """Class representing a person"""

        verbose_name = _("Pul saqlash turi")
        verbose_name_plural = _("Pul saqlash turlari")

    def __str__(self) -> str:
        return self.reester_number
