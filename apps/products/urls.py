from django.urls import path
from apps.products.views import product_list, product_update, product_delete, product_detail,product_add

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("update/<uuid:pk>", product_update, name="update"),
    path("<uuid:pk>/delete/", product_delete, name="delete"),
    path("<uuid:pk>/detail/", product_detail, name="detail"),
    path("add/", product_add, name="add")
]
