from apps.transactions.models import Transaction


def payment_order_generation():
    last_transaction = Transaction.objects.filter(deleted_status=False).last()
    if last_transaction is not None:
        # Transaction exists
        return last_transaction.payment_order + 1
    else:
        return 1


def company_balance_generation(transaction, user):
    balance = user.company.balance
    transaction.company_balance = balance + transaction.balance
    transaction.save()
