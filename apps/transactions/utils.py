from datetime import datetime

from apps.accounts.models import MoneySaver
from apps.orders.models import Order
from apps.transactions.models import Transaction, DoubleEntryAccounting


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def process_updating_entity(transaction, entity):
    update_total_amounts(entity, transaction)


def process_updating_obj_after_transaction(obj, object_name):
    obj.total_debit = generation_total_amount_from_transaction(obj, DoubleEntryAccounting.DEBIT,
                                                               object_name)
    obj.total_credit = generation_total_amount_from_transaction(obj, DoubleEntryAccounting.CREDIT,
                                                                object_name)
    obj.balance = obj.total_debit - obj.total_credit
    obj.save()


def update_total_amounts(obj, transaction):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        obj.total_credit += transaction.balance
        if obj.total_debit > 0:
            obj.balance = obj.total_debit - obj.total_credit
        else:
            obj.balance = 0 - obj.total_credit
    else:
        obj.total_debit += transaction.balance
        if obj.total_credit > 0:
            obj.balance = obj.total_debit - obj.total_credit
        else:
            obj.balance = obj.total_debit - 0
    obj.updated_at = datetime.now()
    obj.save()


def generation_total_amount_from_transaction(obj, double_entry_accounting, object_name):
    from django.db.models import Sum, F
    # Construct the filter using double-underscore notation
    filter_args = {
        f"{object_name}": obj,  # Assuming 'object_name' is the related field name
        'deleted_status': False,
        'double_entry_accounting': double_entry_accounting
    }

    # Your existing query
    result = Transaction.objects.filter(**filter_args).aggregate(
        balance_sum=Sum(F('balance'))
    )

    return result['balance_sum'] or 0


def get_company(user):
    return user.company


def get_order_by_id(id):
    return Order.objects.get(uuid=id)


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, "disconnect")
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, "connect")
    connect(receiver, sender=sender)
