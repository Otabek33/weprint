from django.db import models

from apps.clients.models import Client
from apps.tg.choices import RoleTypeChoices
from django.utils.translation import gettext_lazy as _


class PrintColor(models.IntegerChoices):
    WHITE = 1, _('Oq qora')
    COLOURFUL = 2, _('Rangli')


class PrintSize(models.IntegerChoices):
    A5 = 1, _('A5')
    A4 = 2, _('A4')


class PrintBindingTypes(models.IntegerChoices):
    SPIRAL = 1, _("Cпиральный")
    SADDLE_STITCH = 2, _("Скрипкаланган")
    PERFECT_BINDING = 3, _("китоб")
    CASE = 4, _("Диплом ишига ухшаб")
    PLASTIC_COMB = 5, _("Пласмаса переплет")
    NO_BINDING = 6, _("Переплетсиз")


class DeliveryType(models.IntegerChoices):
    Self_Delivery = 1, _('O\'zim olib ketaman')
    Courier_Delivery = 2, _('Kuryerlik xizmati')


class PaymentType(models.IntegerChoices):
    CASH = 1, _('Naqt')
    CARD = 2, _('Karta orqali')
    WAIT = 3, _('To\'lanmadi')


