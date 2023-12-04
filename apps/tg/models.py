from django.db import models

from apps.clients.models import Client
from apps.tg.choices import RoleTypeChoices
from django.utils.translation import gettext_lazy as _


class PrintColor(models.IntegerChoices):
    WHITE = 1, _('oq qora')
    COLOURFUL = 2, _('rangli')


class PrintSize(models.IntegerChoices):
    A5 = 1, _('A5')
    A4 = 2, _('A4')
    A3 = 3, _('A3')


class PrintBindingTypes(models.IntegerChoices):
    SPIRAL = 1, _("Cпиральный")
    SADDLE_STITCH = 2, _("Скрипкаланган")
    PERFECT_BINDING = 3, _("китоб")
    CASE = 4, _("Диплом ишига ухшаб")
    PLASTIC_COMB = 5, _("Пласмаса переплет")
    NO_BINDING = 6, _("Переплетсиз")


class Theme(models.Model):
    content = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.content


class Chat(models.Model):
    phone = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    subscribers = models.ManyToManyField(Client, blank=True)
    name = models.CharField(max_length=200)
    is_full = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)


class Message(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_role = models.IntegerField(
        "Rol",
        choices=RoleTypeChoices.choices,
        default=RoleTypeChoices.NOT_SPECIFIED,
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True)
    message = models.TextField(blank=True)
    tg_message_id = models.CharField(max_length=100)  # message ni telgramdagi id sini saqlab qolish uchun
    reply_to = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="reply")  # Qaysi message ga javob berilayotganini bilish uchun.
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.chat} / {self.message}"


class TelegramUser(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    tg_pk = models.CharField(max_length=150)
    current_role_in_chat = models.IntegerField(
        "Rol",
        choices=RoleTypeChoices.choices,
        default=RoleTypeChoices.NOT_SPECIFIED,
    )

    def __str__(self) -> str:
        return f"{self.tg_pk}"
