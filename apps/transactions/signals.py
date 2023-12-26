from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transactions.models import Transaction
from apps.transactions.utils import process_updating_company_balance, process_updating_order


@receiver(post_save, sender=Transaction)
def updating_company_balance(sender, instance, created, **kwargs):
    transaction = Transaction.objects.get(id=instance.id)
    process_updating_company_balance(transaction, transaction.company)
    process_updating_order(transaction, transaction.order)
