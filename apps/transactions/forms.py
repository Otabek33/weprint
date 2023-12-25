from django import forms

from apps.clients.models import Client
from apps.orders.models import Order, OrderStatus
from apps.transactions.models import CashType, DoubleEntryAccounting, Transaction


class TransactionCreateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    cash_type = forms.Field(
        widget=forms.Select(
            choices=CashType.choices, attrs={"class": "form-control"}
        ),
    )
    double_entry_accounting = forms.Field(
        widget=forms.Select(
            choices=DoubleEntryAccounting.choices, attrs={"class": "form-control"}
        ),
    )

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control",
            "data-plugin-selectTwo": "",
            "data-plugin-options": '{"minimumInputLength": 2}',
        }),
        required=False,
    )
    # order = forms.ModelChoiceField(
    #     queryset=Order.objects.exclude(order_status=OrderStatus.FINISH),
    #     widget=forms.Select(attrs={"class": "form-control",
    #                                "data-plugin-selectTwo": "",
    #                                "data-plugin-options": '{"minimumInputLength": 2}', }),
    #     required=False,
    # )
    # balance = forms.DecimalField(
    #     widget=forms.NumberInput(attrs={"class": "form-control",}), required=True
    # )

    class Meta:
        model = Transaction
        fields = [
            "description",
            "cash_type",
            "double_entry_accounting",
            "client",
            # "order",
            # "balance",
        ]
