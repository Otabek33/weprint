from django import forms
from apps.tg.models import (PrintSize, PrintColor, PrintBindingTypes)
from apps.orders.models import Order


class OrderCreateForm(forms.ModelForm):
    printSize = forms.Field(
        widget=forms.Select(
            choices=PrintSize.choices, attrs={"class": "form-control"}
        ),
    )
    printColor = forms.Field(
        widget=forms.Select(
            choices=PrintColor.choices, attrs={"class": "form-control"}
        ),
    )
    printBindingType = forms.Field(
        widget=forms.Select(
            choices=PrintBindingTypes.choices, attrs={"class": "form-control"}
        ),
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = Order
        fields = [
            "printSize",
            "printColor",
            "printBindingType",
            "file",
        ]

    widgets = {
        "file": forms.FileInput(attrs={"class": "form-control"}),

    }
