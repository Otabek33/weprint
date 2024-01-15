from django.urls import path

from apps.products.views.binding_type_views import (binding_type_add,
                                                    binding_type_delete,
                                                    binding_type_list,
                                                    binding_type_update)
from apps.products.views.product_views import (product_add, product_delete,
                                               product_detail, product_list,
                                               product_update)

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("update/<uuid:pk>", product_update, name="update"),
    path("<uuid:pk>/delete/", product_delete, name="delete"),
    path("<uuid:pk>/detail/", product_detail, name="detail"),
    path("add/", product_add, name="add"),
    path("<int:pk>/binding_type_list/", binding_type_list, name="binding_type_list"),
    path("<int:pk>/binding-type-add/", binding_type_add, name="binding_type_add"),
    path(
        "<int:pk>/binding-type-delete/", binding_type_delete, name="binding_type_delete"
    ),
    path(
        "<int:pk>/binding-type-update/", binding_type_update, name="binding_type_update"
    ),
]
