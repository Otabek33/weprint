from django import forms
from django.forms import NumberInput
from django.utils.html import format_html, format_html_join

from apps.accounts.models import Company, CashType, MoneySaver


class CurrencyInput(NumberInput):
    def render(self, name, value, attrs=None, renderer=None):
        formatted_value = "{:,.2f}".format(value)  # Format the value as currency
        attrs["readonly"] = "readonly"  # Set the readonly attribute
        attrs["class"] = "form-control"  # Set the readonly attribute

        return format_html(
            '<input{} value="{} so\'m">',
            format_html_join(' ', ' {}="{}"', attrs.items()),
            formatted_value
        )


class CompanyUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    balance = forms.DecimalField(
        widget=CurrencyInput(attrs={"class": "form-control", 'readonly': 'readonly'}), localize=True, required=False,
    )
    total_debit = forms.DecimalField(
        widget=CurrencyInput(attrs={"class": "form-control", 'readonly': 'readonly'}), localize=True, required=False,
    )
    total_credit = forms.DecimalField(
        widget=CurrencyInput(attrs={"class": "form-control", 'readonly': 'readonly'}), localize=True, required=False,
    )

    class Meta:
        model = Company
        fields = [
            "name",
            "address",
            "email",
            "phone",
            "balance",
            "total_debit",
            "total_credit",

        ]


class MoneySaverCreateForm(forms.ModelForm):
    reester_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    cash_type = forms.Field(
        widget=forms.Select(
            choices=CashType.choices, attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = MoneySaver
        fields = [
            "reester_number",
            "cash_type",

        ]
