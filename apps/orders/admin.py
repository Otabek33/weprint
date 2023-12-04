from django.contrib import admin

# Register your models here.
from apps.orders.models import (Order)


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = [
        "created_by",
        # "product",
        "order_number",
        "created_at",
        "file",
        "page_number",
        "price",
        "order_status"

    ]


admin.site.register(Order, OrderAdmin)
