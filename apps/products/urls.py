from django.urls import path
from apps.products.views import product_list, product_add

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("add/", product_add, name="product_create"),
]
