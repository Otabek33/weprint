from django.contrib import admin

# Register your models here.
from apps.products.models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [
        "printSize",
        # "product",
        "printColor",
        "printBindingType",
        "price",
        "company",
        "created_by",
    ]
