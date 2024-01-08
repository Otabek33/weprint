from django import forms
from apps.products.models import (PrintBindingTypes, Product, PrintSize, PrintColor)


class ProductUpdateForm(forms.ModelForm):
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
    printBindingType = forms.ModelChoiceField(
        queryset=PrintBindingTypes.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = Product
        fields = [
            "printSize",
            "printColor",
            "printBindingType",
            "price",

        ]


class ProductCreateForm(forms.ModelForm):
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

    printBindingType = forms.ModelChoiceField(
        queryset=PrintBindingTypes.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = Product
        fields = [
            "printSize",
            "printColor",
            "printBindingType",
            "price",
        ]


class PrintBindingTypesCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = PrintBindingTypes
        fields = [
            "name",
            "photo",

        ]


