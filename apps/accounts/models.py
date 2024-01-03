from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CashType(models.IntegerChoices):
    CASH = 1, _('Naqt')
    BANK = 2, _('Bank')


class UserRole(models.Model):
    """Class representing a person"""

    name = models.CharField("Nomlanishi", blank=True, max_length=55)
    code = models.CharField("Kod", max_length=55)

    class Meta:
        """Class representing a person"""
        verbose_name = "Foydaluvchilar turi"
        verbose_name_plural = "Foydaluvchilar turlari"

    def __str__(self) -> str:
        return str(self.name)


class Company(models.Model):
    """Class representing a person"""

    name = models.CharField("Nomlanishi", blank=True, max_length=55)
    address = models.TextField("Manzil", blank=True, max_length=100)
    email = models.EmailField("Pochta", max_length=100, null=True, blank=True)
    phone = models.CharField("Telefon", max_length=100, null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_debit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        """Class representing a person"""
        verbose_name = "Kompaniya"
        verbose_name_plural = "Kompaniyalar"

    def __str__(self) -> str:
        return str(self.name)


class MoneySaver(models.Model):
    reester_number = models.CharField("Reyester", blank=True, max_length=55)
    cashType = models.IntegerField("Pul turi",
                                   choices=CashType.choices,
                                   default=CashType.CASH)
    balance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name="company_moneySaver", )

    class Meta:
        """Class representing a person"""
        verbose_name = "Pul saqlash turi"
        verbose_name_plural = "Pul saqlash turlari"

    def __str__(self) -> str:
        return str(self.reester_number)


class CustomUser(AbstractUser):
    """Class representing a person"""
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Foydanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    # def get_absolute_url(self):
    #     return reverse("accounts:user-detail", kwargs={"pk": self.id})
    @property
    def is_user(self):
        return self.role.name == 'user'

    @property
    def is_operator(self):
        return self.role.name == 'operator'

    @property
    def is_admin(self):
        """Class representing a person"""
        return self.role.name == 'admin'

    @property
    def is_super_user(self):
        """Class representing a person"""
        return self.role.name == 'superuser'
