from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserRole(models.Model):
    """Class representing a person"""

    name = models.CharField("Наименование", blank=True, max_length=55)
    code = models.CharField("Код", max_length=55)

    class Meta:
        """Class representing a person"""
        verbose_name = "Тип пользователя"
        verbose_name_plural = "Типы пользователей"

    def __str__(self) -> str:
        return str(self.name)


class Company(models.Model):
    """Class representing a person"""

    name = models.CharField("Наименование", blank=True, max_length=55)
    address = models.TextField("Адрес", blank=True, max_length=100)
    email = models.EmailField("Почта", max_length=100, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=100, null=True, blank=True)

    class Meta:
        """Class representing a person"""
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self) -> str:
        return str(self.name)


class CustomUser(AbstractUser):
    """Class representing a person"""
    slug = models.SlugField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to="avatars", default="media/avatars/user.png")

    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

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
