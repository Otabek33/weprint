from django import forms

from apps.orders.models import Order
from apps.tg.models import PrintColor, PrintSize
from apps.orders.models import PrintBindingTypes


class OrderCreateForm(forms.ModelForm):
    printSize = forms.Field(
        widget=forms.Select(choices=PrintSize.choices, attrs={"class": "form-control"}),
    )
    printColor = forms.Field(
        widget=forms.Select(
            choices=PrintColor.choices, attrs={"class": "form-control"}
        ),
    )
    printBindingType = forms.ModelChoiceField(
        queryset=PrintBindingTypes.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=True
    )
    page_number = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=True
    )


    class Meta:
        model = Order
        fields = [
            "printSize",
            "printColor",
            "printBindingType",
            "price",
            "page_number",
        ]
