from django import forms

from apps.accounts.models import MoneySaver
from apps.clients.models import Client
from apps.orders.models import Order, OrderStatus
from apps.transactions.models import DoubleEntryAccounting, Transaction


class TransactionCreateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    cash_type = forms.ModelChoiceField(
        queryset=MoneySaver.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
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

    class Meta:
        model = Transaction
        fields = [
            "description",
            "cash_type",
            "double_entry_accounting",
            "client",

        ]
