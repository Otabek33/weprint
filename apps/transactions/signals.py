from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from apps.transactions.models import Transaction
from apps.transactions.utils import process_updating_entity, process_updating_obj_after_transaction

transaction_deleted_signal = Signal()


@receiver(post_save, sender=Transaction)
def updating_company_balance(sender, instance, created, update_fields, **kwargs):
    transaction = Transaction.objects.get(id=instance.id)
    process_updating_obj_after_transaction(transaction.company, "company")
    if transaction.order:
        process_updating_entity(transaction, transaction.order)

    process_updating_entity(transaction, transaction.client)
    process_updating_entity(transaction, transaction.cash_type)


@receiver(transaction_deleted_signal)
def transaction_deleted_signal_handler(sender, instance, **kwargs):
    process_updating_obj_after_transaction(instance.company, "company")
    if instance.order:
        process_updating_obj_after_transaction(instance.order, "order")
    process_updating_obj_after_transaction(instance.client, "client")
    process_updating_obj_after_transaction(instance.cash_type, "cash_type")
