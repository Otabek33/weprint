from django.contrib import admin

from apps.transactions.models import Transaction


# Register your models here.
@admin.register(Transaction)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "created_at",
        "cash_type",
        "client",
        "order",
        "balance",
        "company_balance",
        "deleted_status",

    ]
    list_editable = ["deleted_status"]
