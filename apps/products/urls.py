from django.urls import path

from apps.products.views.binding_type_views import binding_type_list, binding_type_add
from apps.products.views.product_views import product_list, product_update, product_delete, product_detail, product_add

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("update/<uuid:pk>", product_update, name="update"),
    path("<uuid:pk>/delete/", product_delete, name="delete"),
    path("<uuid:pk>/detail/", product_detail, name="detail"),
    path("add/", product_add, name="add"),
    path("<int:pk>/binding_type_list/", binding_type_list, name="binding_type_list"),
    path("<int:pk>/binding-type-add/", binding_type_add, name="binding_type_add")
]
