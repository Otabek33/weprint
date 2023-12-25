import decimal

from django.db.models.signals import post_save

from apps.accounts.models import Company
from apps.orders.models import Order
from apps.transactions.models import Transaction, CashType, DoubleEntryAccounting


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def company_balance_generation(transaction,price):
    return transaction.company.balance - price \
        if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT \
        else transaction.company.balance + price


def process_updating_company_balance(transaction, company):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        company.balance = transaction.company_balance
    else:
        company.balance = +transaction.company_balance
    company.total_debit = generation_total_amount_from_transaction(company, DoubleEntryAccounting.DEBIT)
    company.total_credit = generation_total_amount_from_transaction(company, DoubleEntryAccounting.CREDIT)
    company.save()


def generation_total_amount_from_transaction(company, double_entry_accounting):
    from django.db.models import Sum
    total_amount = \
        Transaction.objects.filter(company=company, deleted_status=False,
                                   double_entry_accounting=double_entry_accounting).aggregate(
            Sum('balance'))['balance__sum']
    return total_amount


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
