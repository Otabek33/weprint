import decimal

from django.db.models.signals import post_save

from apps.accounts.models import Company
from apps.transactions.models import Transaction, CashType, DoubleEntryAccounting


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def company_balance_generation(transaction):
    return transaction.company.balance - transaction.balance \
        if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT \
        else transaction.company.balance + transaction.balance


def process_updating_company_balance(transaction, company):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        company.balance = transaction.company_balance
    else:
        company.balance = +transaction.company_balance
    company.save()


def generation_header_context(context, user):
    company = user.company
    context['balance'] = company.balance
    context['total_debit'] = company.balance
    context['total_credit'] = company.balance
    return context


def get_company(user):
    return user.company


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, "disconnect")
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, "connect")
    connect(receiver, sender=sender)
