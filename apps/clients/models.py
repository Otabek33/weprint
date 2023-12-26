from django.urls import reverse
from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from apps.accounts.models import CustomUser


# Create your models here.
class Client(models.Model):
    """Class representing a person"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userId = models.CharField(max_length=13, null=True, blank=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    # photo = models.ImageField(upload_to="avatars", default="media/avatars/user.png")
    username = models.CharField(
        _("username"),
        max_length=150,
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="client_created_by",
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="client_updated_by",
    )
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_status = models.BooleanField(default=False)
    total_debit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total_credit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    residual_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("clients:client_list")

    class Meta:
        """Class representing a person"""
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
