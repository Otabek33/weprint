from django.db.models.signals import Signal, post_save, post_delete
from django.dispatch import receiver

from apps.orders.models import Order
from apps.transactions.models import Transaction
from apps.transactions.utils import process_updating_company_balance, process_updating_order, process_updating_client, \
    process_update_transactions

transaction_deleted_signal = Signal()


@receiver(post_save, sender=Transaction)
def updating_company_balance(sender, instance, created, update_fields, **kwargs):
    if update_fields and 'deleted_status' in update_fields:
        # Additional logic when 'deleted_status' field is updated
        transaction_deleted_signal.send(sender=Transaction, instance=instance)
    transaction = Transaction.objects.get(id=instance.id)
    process_updating_company_balance(transaction, transaction.company)
    if transaction.order:
        process_updating_order(transaction, transaction.order)

    process_updating_client(transaction, transaction.client)


@receiver(transaction_deleted_signal)
def transaction_deleted_signal_handler(sender, instance, **kwargs):
    process_update_transactions(instance)
