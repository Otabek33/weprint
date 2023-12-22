import decimal

from apps.accounts.models import Company
from apps.transactions.models import Transaction, CashType


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def company_balance_generation(transaction, user):
    transaction.company_balance = decimal.Decimal(transaction.company.balance + transaction.balance)
    transaction.save()


def process_updating_company_balance(transaction_balance, company):
    company.balance = +transaction_balance
    company.save()


def get_company(user):
    return user.company


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, "disconnect")
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, "connect")
    connect(receiver, sender=sender)
