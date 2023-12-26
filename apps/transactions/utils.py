from datetime import datetime
from apps.orders.models import Order
from apps.transactions.models import Transaction, DoubleEntryAccounting


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def company_balance_generation(transaction, price):
    return transaction.company.balance - price \
        if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT \
        else transaction.company.balance + price


def process_updating_company_balance(transaction, company):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        company.balance = transaction.company_balance
    else:
        company.balance = +transaction.company_balance
    company.total_debit = generation_total_amount_from_transaction(company, DoubleEntryAccounting.DEBIT
                                                                   )
    company.total_credit = generation_total_amount_from_transaction(company, DoubleEntryAccounting.CREDIT
                                                                    )
    company.save()


def process_updating_order(transaction, order):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        order.total_credit = +transaction.balance
        if order.total_debit > 0:
            order.residual_value = order.total_debit - order.total_credit
        else:
            order.residual_value = 0 - order.total_credit
    else:
        order.total_debit = +transaction.balance
        if order.total_credit > 0:
            order.residual_value = order.total_debit - order.total_credit
        else:
            order.residual_value = order.total_debit - 0
    order.save()


def process_updating_client(transaction, client):
    if transaction.double_entry_accounting == DoubleEntryAccounting.CREDIT:
        client.total_credit = +transaction.balance
        if client.total_debit > 0:
            client.residual_value = client.total_debit - client.total_credit
        else:
            client.residual_value = 0 - client.total_credit
    else:
        client.total_debit = +transaction.balance
        if client.total_credit > 0:
            client.residual_value = client.total_debit - client.total_credit
        else:
            client.residual_value = client.total_debit - 0
    client.updated_at = datetime.now()
    client.save()


def generation_total_amount_from_transaction(company, double_entry_accounting):
    from django.db.models import Sum, F
    # Your existing query
    result = Transaction.objects.filter(
        company=company,
        deleted_status=False,
        double_entry_accounting=double_entry_accounting
    ).aggregate(
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
